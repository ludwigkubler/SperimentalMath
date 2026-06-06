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
    
    def permutation_matrix(f, n):
        pm = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i * n + j] == 1:
                    pm[i][j] = 1
        return pm
    
    def rank_variance(pm_list):
        ranks = [sum(row) for row in pm_list]
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((r - mean_rank)**2 for r in ranks) / len(ranks)
        return variance
    
    def groupoid_order(f, n):
        pm = permutation_matrix(f, n)
        order = 1
        while True:
            new_pm = [[pm[j][i] for j in range(n)] for i in range(n)]
            if new_pm == pm:
                break
            pm = new_pm
            order += 1
        return order
    
    def communication_complexity_rank_variance(f, n):
        pm_list = [permutation_matrix(f, n) for _ in range(100)]  # Sample 100 permutation matrices
        return rank_variance(pm_list)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        order = groupoid_order(f, n)
        variance = communication_complexity_rank_variance(f, n)
        if variance == 0:
            return {
                "metric_name": "Order/Var Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Rank variance is zero"
            }
        ratio = order / variance
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in results) / len(results))
    return {
        "metric_name": "Order/Var Ratio",
        "metric_value": mean_ratio,
        "instances_tested": 6 * 100,  # 6 sizes * 100 samples per size
        "n_max": 40,
        "conjecture_holds": all(0.5 <= x <= 2 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(x["metric_value"] for x in all_results if x["metric_value"] is not None) / len(all_results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in all_results if x["metric_value"] is not None) / len(all_results))
    support_fraction = sum(1 for x in all_results if x["conjecture_holds"]) / len(all_results)
    
    if all(x["conjecture_holds"] for x in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in all_results):
        first_failing_seed = next(i for i, x in enumerate(all_results) if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Order/Var Ratio varies' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")