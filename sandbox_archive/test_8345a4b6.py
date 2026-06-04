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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dpll_proof_width(phi):
        # Simplified DPLL algorithm to estimate proof width
        if '0' not in phi and '1' not in phi:
            return 1
        if len(phi) == 1:
            return 1
        p = random.choice('01')
        phi_p = phi.replace(p, '', 1)
        phi_not_p = phi.replace(p, '1' if p == '0' else '0', 1)
        return 2 + max(dpll_proof_width(phi_p), dpll_proof_width(phi_not_p))
    
    def minimal_index_of_representation(n):
        # Simplified calculation of minimal index for demonstration
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_boolean_formula(n)
        min_index = minimal_index_of_representation(n)
        w_DPLL = dpll_proof_width(phi)
        
        if w_DPLL == 0:
            continue
        
        ratio = Fraction(min_index, w_DPLL)
        results.append((n, min_index, w_DPLL, ratio))
    
    if not results:
        return {
            "metric_name": "min_index_over_w_DPLL",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(n for n, _, _, _ in results)
    min_index_over_w_DPLL = sum(ratio.numerator / ratio.denominator for _, _, _, ratio in results) / instances_tested
    
    conjecture_holds = all(2.0 <= ratio <= 1.5 for _, _, _, ratio in results)
    
    return {
        "metric_name": "min_index_over_w_DPLL",
        "metric_value": min_index_over_w_DPLL,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=no_results")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")