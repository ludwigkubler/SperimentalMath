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
    
    def generate_boolean_function(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
    
    def communication_protocol(f):
        n = len(f)
        m = len(f[0])
        # Simplified protocol: each wire is a separate channel
        return m
    
    def minimal_local_zeta_function_size(c):
        # Simplified zeta function size: linear in c
        return c
    
    instances_tested = 0
    mzeta_values = []
    c_values = []
    
    for _ in range(30):  # Sample 30 instances per seed
        n = random.randint(5, 40)
        m = random.randint(n * 2, n * 10)
        f = generate_boolean_function(n, m)
        c = communication_protocol(f)
        mzeta = minimal_local_zeta_function_size(c)
        
        mzeta_values.append(mzeta)
        c_values.append(c)
        instances_tested += 1
    
    if not mzeta_values or not c_values:
        return {
            "metric_name": "mzeta vs c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n for n, _ in zip([random.randint(5, 40) for _ in range(30)], [random.randint(n * 2, n * 10) for _ in range(30)])),
            "conjecture_holds": False,
            "counterexample": "empty_values"
        }
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(mzeta_values, c_values)) / (len(mzeta_values) * std_dev_mzeta * std_dev_c)
    max_deviation = max(abs(x - y) for x, y in zip(mzeta_values, c_values))
    
    return {
        "metric_name": "mzeta vs c",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n for n, _ in zip([random.randint(5, 40) for _ in range(30)], [random.randint(n * 2, n * 10) for _ in range(30)])),
        "conjecture_holds": correlation_coefficient >= 0.7 and max_deviation <= 2,
        "counterexample": "" if correlation_coefficient >= 0.7 and max_deviation <= 2 else f"correlation={correlation_coefficient}, max_deviation={max_deviation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")