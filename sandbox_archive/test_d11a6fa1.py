# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def minimal_rank_quandle_representation(protocol, n):
        # Placeholder for actual implementation
        return 0
    
    def communication_complexity_rank(protocol):
        # Placeholder for actual implementation
        return 0
    
    def pearson_correlation(x, y):
        if len(x) != len(y) or not x:
            return None
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2)) ** 0.5
        if denominator == 0:
            return None
        return numerator / denominator
    
    protocols = [random.randint(1, 40) for _ in range(30)]
    correlation_test = [pearson_correlation([minimal_rank_quandle_representation(p, n) for n in range(5, 41)], 
                                            [communication_complexity_rank(p) for p in range(5, 41)]) for p in protocols]
    
    results = {
        "metric_name": "Pearson correlation",
        "metric_value": sum(correlation_test) / len(correlation_test),
        "instances_tested": len(correlation_test),
        "n_max": 40,
        "conjecture_holds": all(abs(corr) >= 0.8 for corr in correlation_test),
        "counterexample": "" if all(abs(corr) >= 0.8 for corr in correlation_test) else "Pearson correlation < 0.8"
    }
    
    return results

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")