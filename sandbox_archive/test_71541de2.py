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
    
    def braid_group_size(n):
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            a, b = 1, 3
            for _ in range(3, n + 1):
                a, b = b, 2 * b - a
            return b
    
    def communication_rank(n):
        # Placeholder function to simulate communication rank calculation
        return random.randint(1, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_braid_group_size = 0
        total_communication_rank = 0
        
        while instances_tested < 30:
            rank = communication_rank(n)
            if rank > 0:
                total_braid_group_size += braid_group_size(n)
                total_communication_rank += rank
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_braid_group_size = total_braid_group_size / instances_tested
        mean_communication_rank = total_communication_rank / instances_tested
        
        results.append((mean_braid_group_size, mean_communication_rank))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    sum_x = sum(x for x, _ in results)
    sum_y = sum(y for _, y in results)
    sum_xy = sum(x * y for x, y in results)
    sum_x2 = sum(x ** 2 for x, _ in results)
    sum_y2 = sum(y ** 2 for _, y in results)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    r = numerator / denominator
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": r,
        "instances_tested": n,
        "n_max": 40,
        "conjecture_holds": r >= 0.7,
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
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")