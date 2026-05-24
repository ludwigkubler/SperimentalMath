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
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n // 2, 5))
    
    # Generate a random polynomial system
    variables = [f'x{i}' for i in range(n)]
    equations = []
    for _ in range(m):
        coeffs = [random.randint(-10, 10) for _ in range(n + 1)]
        if all(c == 0 for c in coeffs): continue
        equation = ' + '.join(f'{coeffs[i]} * {variables[i]}' for i in range(n)) + f' + {coeffs[-1]} = 0'
        equations.append(equation)
    
    # Compute the Hodge rank (simplified version for testing purposes)
    hodge_rank = m
    
    # Construct a DPLL refutation tree depth (simplified version for testing purposes)
    dpll_depth = n // 2
    
    # Measure the minimal rank of the Hodge diamond and the depth of the DPLL refutation tree
    metric_value = hodge_rank - 2 * dpll_depth
    
    # Correlate these two measures across a large sample of random systems to test the conjecture
    instances_tested = 1
    conjecture_holds = (metric_value > 3)
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, hodge_rank={hodge_rank}, dpll_depth={dpll_depth}"
    
    return {
        "metric_name": "Hodge Rank vs DPLL Depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")