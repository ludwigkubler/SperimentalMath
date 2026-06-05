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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def depth(cnf):
        max_depth = 0
        visited = set()
        
        def dfs(node, current_depth):
            nonlocal max_depth
            if node in visited:
                return
            visited.add(node)
            for clause in cnf:
                if any(abs(clause[var]) == abs(node) for var in range(1, len(clause))):
                    dfs(-node, current_depth + 1)
            max_depth = max(max_depth, current_depth)
        
        for clause in cnf:
            for literal in clause:
                dfs(literal, 0)
        return max_depth
    
    def geometric_quantization_order(cnf):
        n = len(cnf[0])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        
        for i, clause in enumerate(cnf):
            for j, literal in enumerate(clause):
                row = 1 << (abs(literal) - 1)
                if literal > 0:
                    matrix[row][i] += 1
                else:
                    matrix[row][i] -= 1
        
        order = 0
        while any(sum(row) != 0 for row in matrix):
            new_matrix = [[0] * (2**n) for _ in range(2**n)]
            for i in range(2**n):
                if sum(matrix[i]) == 0:
                    continue
                for j in range(2**n):
                    if sum(matrix[j]) == 0:
                        continue
                    new_matrix[i][j] += matrix[i][k] * matrix[k][j]
            matrix = new_matrix
            order += 1
        
        return order
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    OQ_phi = geometric_quantization_order(cnf)
    D_phi = depth(cnf)
    
    if OQ_phi > 10 * D_phi:  # Arbitrary constant c=10 for testing
        conjecture_holds = False
        counterexample = "OQ(φ) > 10 * D(φ)"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "OQ(φ)",
        "metric_value": OQ_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"OQ(φ) > 10 * D(φ)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")