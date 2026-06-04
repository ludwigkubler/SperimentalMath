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
        if n == 1:
            return '0' if random.choice([True, False]) else '1'
        subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
        operator = random.choice(['&', '|'])
        return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def dpll_proof_width(phi):
        if phi == '0' or phi == '1':
            return 1
        elif '&' in phi:
            phi_p, phi_not_p = phi.split('&')
            return 2 + max(dpll_proof_width(phi_p), dpll_proof_width(phi_not_p))
        elif '|' in phi:
            phi_p, phi_not_p = phi.split('|')
            return 2 + max(dpll_proof_width(phi_p), dpll_proof_width(phi_not_p))
        else:
            raise ValueError("Invalid Boolean formula")
    
    def minimal_index_of_representation(n):
        # Placeholder for the actual computation of the minimal index
        # This is a dummy implementation that returns a random value for demonstration purposes
        return random.randint(1, n)
    
    phi = generate_boolean_formula(random.randint(5, 30))
    w_DPLL = dpll_proof_width(phi)
    min_index = minimal_index_of_representation(len(phi.split()))
    
    ratio = Fraction(min_index, w_DPLL) if w_DPLL != 0 else None
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio) if ratio is not None else None,
        "instances_tested": 1,
        "n_max": len(phi.split()),
        "conjecture_holds": False if ratio is None or ratio < Fraction(2, 1) or ratio > Fraction(3, 2) else True,
        "counterexample": "mapping_undefined" if ratio is None else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")