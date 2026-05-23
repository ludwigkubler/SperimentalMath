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
    
    def tropicalize(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] < 0:
                    matrix[i][j] = -matrix[i][j]
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            found_nonzero = False
            for j in range(n):
                if matrix[j][i] != 0:
                    found_nonzero = True
                    break
            if not found_nonzero:
                continue
            rank += 1
            for j in range(n):
                if matrix[j][i] != 0:
                    for k in range(n):
                        matrix[j][k] -= matrix[i][k]
        return rank
    
    def tensor_product(a, b):
        n = len(a)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def acc0_circuit_complexity(matrix):
        n = len(matrix)
        complexity = 0
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    complexity += 1
        return complexity
    
    def generate_instance(n):
        a = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        b = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return tensor_product(a, b)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_instance(n)
        tropicalized = tropicalize(instance)
        rank = min_rank(tropicalized)
        complexity = acc0_circuit_complexity(instance)
        
        if rank > n**2 * math.log(n):
            return {
                "metric_name": "min_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank} > O(n^2 log n)"
            }
        
        if complexity < n**2 * math.log(n):
            return {
                "metric_name": "acc0_circuit_complexity",
                "metric_value": complexity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, complexity={complexity} < O(n^2 log n)"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "complexity": complexity
        })
    
    return {
        "metric_name": "min_rank",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["rank"] <= n**2 * math.log(n) for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    total_metric_value = 0
    total_instances_tested = 0
    conjecture_holds_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        total_instances_tested += trial_result["instances_tested"]
        if trial_result["conjecture_holds"]:
            conjecture_holds_count += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    std_metric_value = (sum((trial_result["metric_value"] - mean_metric_value) ** 2 for trial_result in results) / len(results)) ** 0.5
    support_fraction = conjecture_holds_count / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(trial_result["conjecture_holds"] == False for trial_result in results):
        first_failing_seed = next(seed for seed, trial_result in zip(seeds, results) if not trial_result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={total_instances_tested}")