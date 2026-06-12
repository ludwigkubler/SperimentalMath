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
    
    def hodge_arc_length(zero_locus):
        # Placeholder implementation
        return len(zero_locus)**0.5
    
    def communication_complexity_rank_variance(f):
        # Placeholder implementation
        return sum(f) / len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        zero_locus = [i for i, x in enumerate(f) if x == 0]
        H_f = hodge_arc_length(zero_locus)
        RC_f = communication_complexity_rank_variance(f)
        metrics.append((H_f, RC_f))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in metrics) / len(metrics)
    mean_H_f = sum(x for x, _ in metrics) / len(metrics)
    mean_RC_f = sum(y for _, y in metrics) / len(metrics)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": "" if abs(correlation_coefficient) > 0.7 else "low_correlation"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")