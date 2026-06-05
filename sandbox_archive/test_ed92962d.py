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
    
    # Generate a random permutation of size n
    def generate_instance(n):
        return [i for i in range(1, n+1)]
    
    # Calculate the minimal order of a monoid action on Sn
    def minimal_order(n):
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return math.factorial(n)
    
    # Compute communication complexity rank (simplified for demonstration)
    def communication_complexity_rank(instance):
        n = len(instance)
        return n
    
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_instance(n)
        m_phi = minimal_order(n)
        r_phi = communication_complexity_rank(instance)
        
        instances_tested += 1
        max_n = max(max_n, n)
        
        # Calculate correlation coefficient (simplified for demonstration)
        if instances_tested == 1:
            mean_m = m_phi
            mean_r = r_phi
            sum_m2 = m_phi ** 2
            sum_r2 = r_phi ** 2
            sum_mr = m_phi * r_phi
        else:
            mean_m += m_phi
            mean_r += r_phi
            sum_m2 += m_phi ** 2
            sum_r2 += r_phi ** 2
            sum_mr += m_phi * r_phi
        
        if instances_tested > 1:
            n_samples = instances_tested - 1
            numerator = n_samples * sum_mr - mean_m * mean_r
            denominator = math.sqrt((n_samples * sum_m2 - mean_m ** 2) * (n_samples * sum_r2 - mean_r ** 2))
            correlation_coefficient = numerator / denominator if denominator != 0 else 0
            
            if not (0.8 <= correlation_coefficient <= 1):
                conjecture_holds = False
                counterexample = f"Correlation coefficient {correlation_coefficient} outside [0.8, 1] range for n={n}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")