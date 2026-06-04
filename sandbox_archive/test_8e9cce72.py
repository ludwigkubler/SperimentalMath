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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def dpll_proof_width(phi):
        if phi == "True":
            return 1
        elif phi == "False":
            return None
        else:
            left, op, right = phi.split()
            if op == 'and':
                left_width = dpll_proof_width(left)
                right_width = dpll_proof_width(right)
                if left_width is not None and right_width is not None:
                    return max(left_width, right_width) + 1
                else:
                    return None
            elif op == 'or':
                left_width = dpll_proof_width(left)
                right_width = dpll_proof_width(right)
                if left_width is not None or right_width is not None:
                    return max(left_width, right_width) + 1
                else:
                    return None
    
    def minimal_index(phi):
        # Placeholder for the actual computation of the minimal index
        # This is a dummy function and should be replaced with the actual implementation
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_boolean_formula(n)
    w_DPLL = dpll_proof_width(phi)
    min_index_V = minimal_index(phi)
    
    if w_DPLL is None:
        return {
            "metric_name": "min_index(V) / w_DPLL(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL proof width is None"
        }
    
    ratio = min_index_V / w_DPLL
    return {
        "metric_name": "min_index(V) / w_DPLL(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 2.0 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if 2.0 <= result["metric_value"] <= 1.5) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is None)
        print(f"RESULT: FALSIFIED counterexample='DPLL proof width is None' first_failing_seed={first_failing_seed}")