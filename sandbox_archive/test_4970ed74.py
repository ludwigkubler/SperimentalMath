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
    
    def log_base(x, base):
        if x <= 0 or base <= 1:
            return None
        return math.log(x) / math.log(base)
    
    def communication_complexity(n):
        # Placeholder function for communication complexity
        return n * log_base(n, 2)
    
    def geometric_entropy(n):
        # Placeholder function for geometric entropy
        return log_base(n, 2)
    
    def ratio(n):
        alpha = 1.0
        beta = 2.0
        f_n = alpha * log_base(beta**n, 2)
        g_n = log_base(beta**n, 2)
        return f_n / g_n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cc = communication_complexity(n)
        ge = geometric_entropy(n)
        if cc is None or ge is None:
            continue
        results.append((n, cc, ge))
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    total_ratio = sum(r[1] / r[2] for n, cc, ge in results)
    mean_ratio = total_ratio / len(results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": abs(mean_ratio - 1) < 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Ratio does not remain constant"
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)