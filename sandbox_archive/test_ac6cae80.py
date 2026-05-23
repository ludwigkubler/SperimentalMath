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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_convolution_matrix(f):
        n = len(f)
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i & j] == 1:
                    M[i][j] += 1
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for row in matrix:
            non_zero_row = any(row[j] != 0 for j in range(n))
            if non_zero_row:
                rank += 1
        return rank
    
    def bp_read_twice_width(f):
        # Placeholder function, as the actual implementation is complex and not provided
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = free_convolution_matrix(f)
        rank = min_rank(M)
        bp_width = bp_read_twice_width(f)
        
        if rank < 0.9 * (n ** 0.5) or rank > 1.1 * (n ** 0.5):
            return {
                "metric_name": "Minimal Rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Failed for n={n}, rank={rank}"
            }
        
        if bp_width > 2:
            return {
                "metric_name": "BP_ReadTwice Width",
                "metric_value": bp_width,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Failed for n={n}, width={bp_width}"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "width": bp_width
        })
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": sum(result["rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(0.9 * (n ** 0.5) <= rank <= 1.1 * (n ** 0.5) for n, rank, _ in results) and all(width <= 2 for _, _, width in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    total_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_results.append(result)
    
    supports = sum(result["conjecture_holds"] for result in total_results)
    mean_rank = sum(result["metric_value"] for result in total_results) / len(total_results)
    std_rank = (sum((result["metric_value"] - mean_rank)**2 for result in total_results) / len(total_results))**0.5
    
    if supports >= 0.8 * len(seeds):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={supports/len(seeds)}")
    elif any(not result["conjecture_holds"] for result in total_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, total_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")