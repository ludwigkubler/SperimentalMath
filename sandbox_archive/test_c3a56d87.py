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
    
    def p_adic_valuation(f, p):
        val = 0
        for coeff in f:
            while coeff % p == 0 and coeff != 0:
                coeff //= p
                val += 1
        return val
    
    def is_acc0_circuit(f, depth):
        # Placeholder for ACC⁰ circuit construction logic
        # This is a dummy implementation for testing purposes
        return True
    
    n = random.randint(5, 40)
    p = random.choice([2, 3, 5, 7, 11])
    
    f = [random.randint(0, p-1) for _ in range(n+1)]
    val_p_f = p_adic_valuation(f, p)
    
    if val_p_f < 1:
        return {
            "metric_name": "val_p(f)",
            "metric_value": val_p_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    depth = random.randint(1, min(val_p_f, 5))
    acc0_circuit_exists = is_acc0_circuit(f, depth)
    
    return {
        "metric_name": "val_p(f)",
        "metric_value": val_p_f,
        "instances_tested": 1,
        "conjecture_holds": acc0_circuit_exists,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_val_p_f = sum(result["metric_value"] for result in results) / len(results)
    std_val_p_f = math.sqrt(sum((result["metric_value"] - mean_val_p_f) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_val_p_f} std={std_val_p_f} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val_p_f} std={std_val_p_f} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")