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
        for _ in range(2 ** n):
            clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)]
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
                if all(abs(lit) == node for lit in clause):
                    max_depth = max(max_depth, current_depth + 1)
                    for other_lit in clause:
                        dfs(-other_lit, current_depth + 1)
        
        for i in range(1, n + 1):
            dfs(i, 0)
            dfs(-i, 0)
        return max_depth
    
    def geometric_quantization_order(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        
        for clause in cnf:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    matrix[i][i] += 1
                else:
                    matrix[i][i] -= 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                
                factor = A[i][i]
                for j in range(n):
                    A[i][j] /= factor
                
                for j in range(m):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
            
            return A
        
        gaussian_elimination(matrix)
        
        order = 0
        for row in matrix:
            for val in row:
                if val != 0:
                    order += 1
                    break
        return order
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    oq_phi = geometric_quantization_order(cnf)
    d_phi = depth(cnf)
    
    c = 2  # Example constant, adjust as needed
    expected_bound = c * d_phi
    
    return {
        "metric_name": "OQ(φ) / D(φ)",
        "metric_value": oq_phi / d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": oq_phi <= expected_bound,
        "counterexample": "" if oq_phi <= expected_bound else f"OQ({oq_phi}) > {c} * D({d_phi})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        counterexample_desc = f"OQ({results[first_failing_seed]['metric_value']}) > {2} * D({results[first_failing_seed]['instances_tested']})"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")