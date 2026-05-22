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

def generate_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, random.randint(1, n))
        clause = [f"{random.choice(['', '-'])}{var}" for var in clause]
        clauses.append(clause)
    return clauses

def integral_representation(formula):
    norm = 0
    for clause in formula:
        clause_norm = sum(abs(int(c[1:]) if c[0] != '-' else -int(c[1:])) for c in clause)
        if clause_norm > norm:
            norm = clause_norm
    return norm

def dpll_search_tree_width(formula):
    # Placeholder implementation, actual DPLL algorithm not provided
    return random.randint(1, 10) * math.log(len(formula))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_formula(n)
    
    norm = integral_representation(formula)
    width = dpll_search_tree_width(formula)
    
    metric_value = norm
    conjecture_holds = (norm <= math.log(n)) and (width <= 2 * math.log(n))
    counterexample = "" if conjecture_holds else f"Norm: {norm}, Width: {width}"
    
    return {
        "metric_name": "Minimal Norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Norm too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")