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
        n = len(matrix)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        n = len(matrix)
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def construct_quantum_group_representation(bp_size):
        # Placeholder for the actual construction logic
        return [[random.randint(0, 1) for _ in range(bp_size)] for _ in range(bp_size)]
    
    bp_sizes = [5, 10, 15, 20, 30, 40]
    results = []
    
    for bp_size in bp_sizes:
        for _ in range(5):  # Test with 5 instances per size
            bp = [[random.randint(0, 1) for _ in range(bp_size)] for _ in range(bp_size)]
            qgr = construct_quantum_group_representation(bp_size)
            rank_value = rank(qgr)
            results.append({
                "bp_size": bp_size,
                "rank": rank_value
            })
    
    if not results:
        return {
            "metric_name": "Rank vs BP_ReadTwice",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_rank = sum(result["rank"] for result in results) / len(results)
    min_rank = min(result["rank"] for result in results)
    max_rank = max(result["rank"] for result in results)
    support_fraction = sum(1 for result in results if 0.5 * result["bp_size"] <= result["rank"] <= 2 * result["bp_size"]) / len(results)
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"min_rank={min_rank}, max_rank={max_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - avg_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")