# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_circuit(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate literals
        literals = [random.choice(variables + [f'~{v}' for v in variables]) for _ in range(m)]
        
        # Generate clauses
        for literal in literals:
            if literal.startswith('~'):
                clause = [literal[1:], random.choice(variables), random.choice(variables)]
            else:
                clause = [literal, random.choice(variables + [f'~{v}' for v in variables])]
            clauses.append(clause)
        
        return variables, clauses
    
    def geometric_quantization_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        
        # Initialize the matrix
        Q = [[0] * (n + 1) for _ in range(m)]
        
        # Fill the matrix based on the Tseitin circuit
        for i, clause in enumerate(clauses):
            if clause[0].startswith('~'):
                var_index = variables.index(clause[0][1:]) + 1
                Q[i][var_index] = -1
            else:
                var_index = variables.index(clause[0]) + 1
                Q[i][var_index] = 1
            
            if clause[1].startswith('~'):
                var_index = variables.index(clause[1][1:]) + 1
                Q[i][var_index] = -1
            else:
                var_index = variables.index(clause[1]) + 1
                Q[i][var_index] = 1
            
            if clause[2].startswith('~'):
                var_index = variables.index(clause[2][1:]) + 1
                Q[i][var_index] = -1
            else:
                var_index = variables.index(clause[2]) + 1
                Q[i][var_index] = 1
        
        return Q
    
    def minimal_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        
        # Gaussian elimination to find the rank
        for i in range(n):
            if matrix[i][i] == 0:
                found = False
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    return i
        
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(m):
                        matrix[j][k] += factor * matrix[i][k]
        
        return n
    
    def phi_c(matrix):
        rank = minimal_rank(matrix)
        m = len(matrix)
        n = len(matrix[0])
        expected = m**2 * math.log(n)
        return abs(rank - expected) / expected <= 0.3
    
    results = []
    for n in [30, 40]:
        for m in [100, 200]:
            variables, clauses = generate_tseitin_circuit(n, m)
            Q = geometric_quantization_matrix(variables, clauses)
            rank = minimal_rank(Q)
            if not phi_c(Q):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Tseitin circuit with n={n}, m={m} failed"
                }
            results.append(rank)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.7 * (m**2 * math.log(n)) and r <= 1.3 * (m**2 * math.log(n))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")