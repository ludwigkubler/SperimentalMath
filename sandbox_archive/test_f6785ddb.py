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

def random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def geometric_entropy(f):
    n = int(math.log2(len(f)))
    counts = [f.count(i) for i in range(2)]
    probabilities = [c / len(f) for c in counts]
    entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
    return entropy

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    protocol = [(i, f[i]) for i in range(2**n)]
    rank = len(set(f))
    variance = (rank - 1) / (2**n - 1)
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = random_boolean_function(n)
        mge_f = geometric_entropy(f)
        rcv_f = communication_complexity_rank_variance(f)
        results.append({"n": n, "mge_f": mge_f, "rcv_f": rcv_f})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mge_values = [r["mge_f"] for r in results]
    rcv_values = [r["rcv_f"] for r in results]
    mean_mge = sum(mge_values) / len(mge_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    
    correlation = sum((mge - mean_mge) * (rcv - mean_rcv) for mge, rcv in zip(mge_values, rcv_values)) / (len(results) * math.sqrt(sum((mge - mean_mge)**2 for mge in mge_values) * sum((rcv - mean_rcv)**2 for rcv in rcv_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation) >= 0.8 and all(abs(mge - mean_mge) <= 3 for mge in mge_values),
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
    
    mean_correlation = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_correlation = math.sqrt(sum((r["metric_value"] - mean_correlation)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")