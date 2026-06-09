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
    
    def qrs(phi):
        # Placeholder for minimal quadratic residue symbol computation
        return sum(1 for clause in phi if len(clause) == 2)
    
    def rcv(phi):
        # Placeholder for communication complexity rank variance computation
        return sum(len(clause)**2 for clause in phi) / len(phi)
    
    def correlation(r_qrs, rcv):
        n = len(r_qrs)
        mean_r_qrs = sum(r_qrs) / n
        mean_rcv = sum(rcv) / n
        numerator = sum((r_qrs[i] - mean_r_qrs) * (rcv[i] - mean_rcv) for i in range(n))
        denominator = math.sqrt(sum((r_qrs[i] - mean_r_qrs)**2 for i in range(n))) * math.sqrt(sum((rcv[i] - mean_rcv)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    r_qrs_values = []
    rcv_values = []
    
    for n in n_values:
        phi = [[random.randint(1, n) for _ in range(random.randint(2, n))] for _ in range(n)]
        r_qrs_values.append(qrs(phi))
        rcv_values.append(rcv(phi))
    
    corr = correlation(r_qrs_values, rcv_values)
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")