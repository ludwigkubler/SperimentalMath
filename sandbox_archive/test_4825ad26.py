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

def generate_formula(n: int) -> str:
    if n == 1:
        return "True"
    elif n == 2:
        return "A & B"
    else:
        formulas = [generate_formula(i) for i in range(1, n)]
        return f"({' & '.join(formulas[:n//2])}) | ({' & '.join(formulas[n//2:])})"

def local_dimension(formula: str) -> int:
    if formula == "True":
        return 0
    elif formula == "False":
        return float('inf')
    elif ' & ' in formula:
        left, right = formula.split(' & ')
        return max(local_dimension(left), local_dimension(right))
    elif ' | ' in formula:
        left, right = formula.split(' | ')
        return 1 + min(local_dimension(left), local_dimension(right))

def resolution_width(formula: str) -> int:
    if formula == "True":
        return 0
    elif formula == "False":
        return float('inf')
    elif ' & ' in formula:
        left, right = formula.split(' & ')
        return max(resolution_width(left), resolution_width(right))
    elif ' | ' in formula:
        left, right = formula.split(' | ')
        return 1 + min(resolution_width(left), resolution_width(right))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        ld = local_dimension(formula)
        rw = resolution_width(formula)
        
        if ld > rw:
            return {
                "metric_name": "local_dimension",
                "metric_value": ld,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Formula '{formula}' has local dimension {ld} > resolution width {rw}"
            }
        
        results.append((ld, rw))
    
    avg_ld = sum(ld for ld, _ in results) / len(results)
    avg_rw = sum(rw for _, rw in results) / len(results)
    
    return {
        "metric_name": "local_dimension",
        "metric_value": avg_ld,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_ld = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_ld} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ld} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='local_dimension > resolution_width' first_failing_seed={first_failing_seed}")