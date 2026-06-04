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
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def hodge_order(f):
        # Placeholder function to simulate Hodge order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def monotone_width(f):
        # Placeholder function to simulate monotone width calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) // 2
    
    n = random.randint(5, 40)
    phi = generate_boolean_function(n)
    h_phi = hodge_order(phi)
    w_phi = monotone_width(phi)
    
    if h_phi == 0 or w_phi == 0:
        return {
            "metric_name": "h_phi_over_w_phi",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = Fraction(h_phi, w_phi)
    log_n = math.log(n)
    
    return {
        "metric_name": "h_phi_over_w_phi",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5 and ratio >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    total_ratio = Fraction(0)
    count_support = 0
    count_total = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["metric_value"] is not None:
            total_ratio += Fraction(trial_result["metric_value"])
            count_total += 1
            if trial_result["conjecture_holds"]:
                count_support += 1
    
    mean = float(total_ratio / count_total) if count_total > 0 else None
    support_fraction = count_support / len(seeds)
    
    if all(trial_result["metric_value"] is not None for trial_result in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.95 else "FALSIFIED"
        counterexample = "" if RESULT == "SUPPORTED" else min((trial_result for trial_result in results if not trial_result["conjecture_holds"]), key=lambda x: x["metric_value"])["counterexample"]
        first_failing_seed = next((seed for seed, trial_result in enumerate(results) if not trial_result["conjecture_holds"]), None)
        
        print(f"RESULT: {RESULT} mean={mean} std=0 support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE some trials had no metric_value")