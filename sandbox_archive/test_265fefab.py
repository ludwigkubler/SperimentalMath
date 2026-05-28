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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice(['x', '~x']) + str(i+1) for i in range(n)]
            random.shuffle(clause)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def parse_xor_3cnf(formula):
        literals = set()
        for clause in formula.split(' and '):
            for literal in clause.split(' or '):
                if literal.startswith('~'):
                    literals.add(literal[1:])
                else:
                    literals.add(literal)
        return literals
    
    def construct_quadratic_form(literals):
        n = len(literals)
        q = [[0] * n for _ in range(n)]
        for literal in literals:
            i = int(literal[1:]) - 1
            if literal.startswith('~'):
                q[i][i] += 1
            else:
                q[i][i] -= 1
        return q
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def construct_monomial_circuit(formula):
        n = len(parse_xor_3cnf(formula))
        circuit_size = 2**(n-1) + n - 1
        return circuit_size
    
    def compute_ratio(q, circuit_size):
        rank = gaussian_elimination(q)
        if rank is None:
            return None
        return Fraction(rank, circuit_size)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_xor_3cnf(n)
    literals = parse_xor_3cnf(formula)
    q = construct_quadratic_form(literals)
    circuit_size = construct_monomial_circuit(formula)
    
    if q is None or circuit_size is None:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = compute_ratio(q, circuit_size)
    if ratio is None:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")