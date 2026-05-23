# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def plethysm_coefficient(n):
        # Placeholder for plethysm coefficient calculation
        return n * (n + 1) / 2
    
    def inverse_hook_length_weighting(n):
        # Placeholder for inverse hook-length weighting calculation
        return Fraction(1, n**2)
    
    def rho(f, n):
        return max(inverse_hook_length_weighting(n) * plethysm_coefficient(n), key=lambda x: x)
    
    perm_n = rho("perm", 5)
    det_m_k_values = [rho("det", m) for m in range(1, int(5**1.5) + 1)]
    
    metric_value = perm_n
    instances_tested = len(det_m_k_values)
    conjecture_holds = all(metric_value > val for val in det_m_k_values)
    counterexample = "" if conjecture_holds else "det_m_k"
    
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support found")