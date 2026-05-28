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
    
    def generate_polynomial(n):
        coeffs = [random.choice([-1, 1]) for _ in range(n+1)]
        return coeffs
    
    def evaluate_polynomial(poly, x_values):
        n = len(poly) - 1
        values = []
        for x_val in x_values:
            value = sum(c * (x_val ** i) for i, c in enumerate(reversed(poly)))
            values.append(value)
        return values
    
    def is_parity_function(values):
        return all(v % 2 == int(x % 2) for v, x in zip(values, range(len(values))))
    
    def compute_rank(poly, n):
        # Simple heuristic to estimate rank (not rigorous)
        return len(set(evaluate_polynomial(poly, range(2**n))))
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    x_values = [i for i in range(2**n)]
    values = evaluate_polynomial(poly, x_values)
    
    if not is_parity_function(values):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "The polynomial does not define the Parity function."
        }
    
    rank = compute_rank(poly, n)
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"The polynomial does not define the Parity function.\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")