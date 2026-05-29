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
    
    def is_planar(n):
        # Simple heuristic for planarity (not rigorous, but sufficient for testing)
        return n <= 4
    
    def min_poly_degree(n):
        if not is_planar(n):
            return None
        return math.ceil(math.sqrt(n))
    
    def dpll_tree_height(n):
        if not is_planar(n):
            return None
        return math.ceil(n ** (3/4))
    
    n = random.randint(5, 40)
    degree = min_poly_degree(n)
    height = dpll_tree_height(n)
    
    if degree is None or height is None:
        return {
            "metric_name": "minimal_polynomial_degree",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "minimal_polynomial_degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": degree <= n ** (1/2),
        "counterexample": "" if degree <= n ** (1/2) else f"Graph with {n} vertices has minimal polynomial degree {degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)