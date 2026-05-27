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
        literals = [f'{var}^' if random.choice([True, False]) else var for var in variables]
        
        # Generate clauses
        for _ in range(m):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        
        return variables, clauses
    
    def geometric_quantization_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Fill the matrix
        for i in range(m):
            x1, x2 = clauses[i]
            if '^' in x1:
                var1 = x1[:-1]
                sign1 = -1 if x1[-1] == '^' else 1
            else:
                var1 = x1
                sign1 = 1
            
            if '^' in x2:
                var2 = x2[:-1]
                sign2 = -1 if x2[-1] == '^' else 1
            else:
                var2 = x2
                sign2 = 1
            
            Q[variables.index(var1)][variables.index(var2)] += sign1 * sign2
        
        return Q
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    n_values = [30, 40]
    m_values = [100, 200]
    
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for m in m_values:
            variables, clauses = generate_tseitin_circuit(n, m)
            Q = geometric_quantization_matrix(variables, clauses)
            rank = min_rank(Q)
            total_rank += rank
            instances_tested += 1
    
    expected_rank = sum(m**2 * math.log(n) for n in n_values for m in m_values)
    
    if abs(total_rank - expected_rank) <= 0.3 * expected_rank:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Rank {total_rank} does not fall within ±30% of Θ(m^2 log n)"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": total_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")