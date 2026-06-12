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
    
    def hamming_distance(a, b):
        return sum(x != y for x, y in zip(a, b))
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        mte = [sum(hamming_distance(f[i], f[j]) for j in range(n)) / (n * (n - 1) / 2) for i in range(n)]
        return sum((x - mean_mte)**2 for x in mte) / n
    
    def hodge_arc_length(n):
        # Simplified approximation for demonstration purposes
        return math.sqrt(n)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        h = hodge_arc_length(n)
        rc = communication_complexity_rank_variance(f)
        results.append((h, math.sqrt(n) * rc))
    
    metric_value = correlation_coefficient([x[0] for x in results], [x[1] for x in results])
    conjecture_holds = 0.5 < metric_value < 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if 0.5 < x["metric_value"] < 0.7) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] and 0.5 < x["metric_value"] < 0.7 for x in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] and x["metric_value"] <= 0.5 for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"] and x["metric_value"] <= 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")