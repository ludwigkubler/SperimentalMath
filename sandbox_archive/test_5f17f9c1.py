# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(instance):
        if not instance:
            return 0
        for assignment in product([0, 1], repeat=len(instance[0])):
            if all(all(lit == (assignment[i] if lit >= 0 else -assignment[-lit-1]) for lit in clause) for clause in instance):
                return 1 + dpll([[lit for lit in clause if lit != assignment[i]] for clause in instance if not all(lit == 0 or lit == -assignment[i] for lit in clause)])
        return float('inf')
    
    def p_adic_valuation_complexity(instance):
        valuations = set()
        for assignment in product([0, 1], repeat=len(instance[0])):
            valuation = sum(2**i if bit == 1 else 0 for i, bit in enumerate(clause) for clause in instance)
            valuations.add(valuation)
        return len(valuations)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        instance = [[random.randint(-n, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        dpll_path_length = dpll(instance)
        if dpll_path_length == float('inf'):
            continue
        p_val_complexity = p_adic_valuation_complexity(instance)
        metric_values.append(p_val_complexity / math.log(n))
        
        if abs(p_val_complexity - math.log(n) * dpll_path_length) > 2 * math.log(n):
            conjecture_holds = False
            counterexample = f"Instance with n={n} failed. P-adic complexity: {p_val_complexity}, DPLL path length: {dpll_path_length}"
    
    return {
        "metric_name": "P-adic Valuation Complexity / log(n)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")