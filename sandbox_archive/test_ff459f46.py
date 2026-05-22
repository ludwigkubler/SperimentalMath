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
    
    def generate_cnf(n, k):
        clauses = []
        for i in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = rank
            for i in range(rank, rows):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] != 0:
                matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
                for i in range(rank + 1, rows):
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(cols):
                        if j <= k:
                            matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def compute_minimal_intersection_rank(cnf):
        n = len(cnf)
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    variables.add(literal)
                else:
                    variables.add(-literal)
        m = len(variables)
        matrix = [[0] * (m + 1) for _ in range(m)]
        var_map = {var: i for i, var in enumerate(variables)}
        
        for clause in cnf:
            literals = [abs(lit) for lit in clause if abs(lit) in var_map]
            for i in range(len(literals)):
                for j in range(i + 1, len(literals)):
                    matrix[var_map[literals[i]]][var_map[literals[j]]] += 1
                    matrix[var_map[literals[j]]][var_map[literals[i]]] += 1
        
        return gaussian_elimination(matrix)
    
    def construct_monotone_circuit(n, k):
        # This is a placeholder for the actual circuit construction logic.
        # For simplicity, we assume a trivial circuit with depth n^k.
        return n ** k
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            cnf = generate_cnf(n, k)
            rank = compute_minimal_intersection_rank(cnf)
            depth = construct_monotone_circuit(n, k)
            total_rank += rank
            total_depth += depth
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_depth = total_depth / instances_tested
    
    if mean_depth == 0:
        return {
            "metric_name": "Ratio of Mean Minimal Intersection Rank to Mean Monotone Circuit Depth",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    ratio = mean_rank / mean_depth
    return {
        "metric_name": "Ratio of Mean Minimal Intersection Rank to Mean Monotone Circuit Depth",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")