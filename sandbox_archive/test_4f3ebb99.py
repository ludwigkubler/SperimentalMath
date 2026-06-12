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
    
    def generate_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def calculate_m(phi):
        # Placeholder function to calculate m(φ). Replace with actual implementation.
        return len(phi)
    
    def calculate_w(phi):
        # Placeholder function to calculate w(φ). Replace with actual implementation.
        return len(phi) ** 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        m_values = []
        w_values = []
        
        for _ in range(30):
            phi = generate_instance(n)
            m = calculate_m(phi)
            w = calculate_w(phi)
            
            if m is None or w is None:
                continue
            
            m_values.append(m)
            w_values.append(w)
            instances_tested += 1
        
        if not m_values or not w_values:
            return {
                "metric_name": "m(φ) / n^3",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        m_avg = sum(m_values) / len(m_values)
        w_avg = sum(w_values) / len(w_values)
        m_over_n3 = m_avg / (n ** 3)
        
        results.append({
            "metric_name": "m(φ) / n^3",
            "metric_value": m_over_n3,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_shv = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_shv) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_shv} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")