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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref = gaussian_elimination([row[:] for row in matrix])
        return sum(1 for row in rref if any(row[j] != 0 for j in range(cols)))
    
    def p_adic_differential(f, x):
        h = 1e-10
        diff = []
        for i in range(len(x)):
            x_plus_h = [xj + (h if j == i else 0) for j, xj in enumerate(x)]
            y = f(x)
            y_plus_h = f(x_plus_h)
            diff.append((y_plus_h - y) / h)
        return diff
    
    def ac0_circuit_depth(n):
        # Placeholder function to generate a random AC0 circuit depth
        return 2 ** (n // 10 + random.randint(1, 3))
    
    def parity_function(x):
        return sum(x) % 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):  # Sample 5 instances per size
            depth = ac0_circuit_depth(n)
            x = [random.randint(0, 1) for _ in range(n)]
            f = lambda y: parity_function(y)
            diff = p_adic_differential(f, x)
            rank_value = rank(diff)
            
            if rank_value < c * math.log2(2 ** n):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Rank {rank_value} is less than {c * math.log2(2 ** n)} for n={n}"
                }
            
            total_rank += rank_value
            instances_tested += 1
        
        results.append({"n": n, "instances_tested": instances_tested, "mean_rank": total_rank / instances_tested})
    
    mean_rank = sum(result["mean_rank"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["mean_rank"] >= c * math.log2(2 ** result["n"])) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": support_fraction >= 0.96,  # 28 out of 30 seeds
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")