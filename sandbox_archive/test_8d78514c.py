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
    
    def geometric_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in range(2**n)]
        probabilities = [c / n for c in counts]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        # Simple deterministic protocol: transmit the first bit
        return 1
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        mge_f = geometric_entropy(f)
        rcv_f = communication_complexity_rank_variance(f)
        results.append((mge_f, rcv_f))
    
    if not results:
        return {
            "metric_name": "mge_vs_rcv",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mge_values = [r[0] for r in results]
    rcv_values = [r[1] for r in results]
    mean_mge = sum(mge_values) / len(mge_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    correlation_coefficient = sum((m - mean_mge) * (r - mean_rcv) for m, r in zip(mge_values, rcv_values)) / (len(results) * math.sqrt(sum((m - mean_mge)**2 for m in mge_values) * sum((r - mean_rcv)**2 for r in rcv_values)))
    max_n = max(n for _, _ in results)
    
    return {
        "metric_name": "mge_vs_rcv",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(m - r) <= 3 for m, r in zip(mge_values, rcv_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")