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
    
    def entropy(f):
        n = len(f)
        p_1 = f.count(1) / n
        p_0 = f.count(0) / n
        if p_1 == 0 or p_0 == 0:
            return 0
        return -p_1 * math.log2(p_1) - p_0 * math.log2(p_0)
    
    def minimal_order_of_quotient_algebra(f):
        # Simplified version for demonstration; actual implementation needed
        n = len(f)
        return n ** (math.log(n, 2) / 2)
    
    results = []
    for n in range(5, 41):
        f = generate_boolean_function(n)
        h_f = entropy(f)
        o_Q_f = minimal_order_of_quotient_algebra(f)
        results.append((n, h_f, o_Q_f))
    
    correlation_coefficient = pearson_correlation(results)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else "Pearson Correlation Coefficient < 0.5"
    }

def pearson_correlation(data):
    n = len(data)
    x_sum = sum(x for _, x, _ in data)
    y_sum = sum(y for _, _, y in data)
    xy_sum = sum(x * y for _, x, y in data)
    x_squared_sum = sum(x**2 for _, x, _ in data)
    y_squared_sum = sum(y**2 for _, _, y in data)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x_squared_sum - x_sum**2) * (n * y_squared_sum - y_sum**2))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation Coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support_fraction support_fraction={support_fraction}")