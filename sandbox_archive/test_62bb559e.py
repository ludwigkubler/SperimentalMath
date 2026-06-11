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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank_var = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank_var += 1
        return rank_var
    
    def minimal_index_of_crossed_product(f):
        n = len(f)
        # Simplified approximation for demonstration purposes
        return math.log(n) * math.log(n)**2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        rank_var = communication_complexity_rank_variance(f)
        I_n = minimal_index_of_crossed_product(f)
        
        if rank_var == 0:
            continue
        
        ratio = I_n / rank_var
        results.append((n, ratio))
    
    if not results:
        return {
            "metric_name": "I(n)/r(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _ in results)
    if n_max < 16:
        return {
            "metric_name": "I(n)/r(n)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    ratios = [ratio for _, ratio in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio)**2 for r in ratios) / len(ratios))
    
    return {
        "metric_name": "I(n)/r(n)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(1.5 >= ratio for _, ratio in results) and std_ratio > 0.8 * math.log(n_max) * math.log(n_max)**2,
        "counterexample": "" if all(1.5 >= ratio for _, ratio in results) else f"ratio={max(ratio for _, ratio in results)} exceeds 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")