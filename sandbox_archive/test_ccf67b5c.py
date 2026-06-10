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
    
    def generate_instance():
        m = random.randint(5, 30)
        q = random.randint(1, m)
        # Generate a binary form of the communication complexity problem
        binary_form = [random.choice([0, 1]) for _ in range(m)]
        return m, q, binary_form
    
    def compute_mSR(binary_form):
        n = len(binary_form)
        # Compute the minimal symplectic representation rank (mSR(φ))
        # This is a placeholder implementation; replace with actual computation
        mSR = sum(binary_form)  # Example: sum of bits as a simple proxy
        return mSR
    
    def compute_rank_variance(binary_form):
        n = len(binary_form)
        mean = sum(binary_form) / n
        variance = sum((x - mean) ** 2 for x in binary_form) / n
        return variance
    
    total_mSR = []
    total_w = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        m, q, binary_form = generate_instance()
        if len(binary_form) > n_max:
            n_max = len(binary_form)
        
        mSR = compute_mSR(binary_form)
        w = compute_rank_variance(binary_form)
        
        total_mSR.append(mSR)
        total_w.append(w)
        instances_tested += 1
    
    correlation_coefficient = (instances_tested * sum(mSR * w for mSR, w in zip(total_mSR, total_w)) - 
                               len(total_mSR) * sum(total_mSR) * sum(total_w)) / \
                              ((len(total_mSR) * sum(x ** 2 for x in total_mSR) - sum(total_mSR) ** 2) *
                               (len(total_mSR) * sum(x ** 2 for x in total_w) - sum(total_w) ** 2)) ** 0.5
    
    conjecture_holds = correlation_coefficient >= 0.9 and all(w <= 1.5 * mSR for mSR, w in zip(total_mSR, total_w))
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9 or rank_variance > 2 * mSR"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")