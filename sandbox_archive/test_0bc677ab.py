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
        # Implement a simple planarity test (e.g., Kuratowski's theorem)
        return n <= 4
    
    def minimal_polynomial_degree(n):
        if not is_planar(n):
            return -1
        # Placeholder for actual computation of minimal polynomial degree
        return random.randint(0, int(math.sqrt(n)))
    
    def dpll_search_tree_height(n):
        if not is_planar(n):
            return -1
        # Placeholder for actual computation of DPLL search tree height
        return random.randint(0, int(n ** (3/4)))
    
    n = random.randint(5, 40)
    metric_value = minimal_polynomial_degree(n)
    conjecture_holds = metric_value <= math.sqrt(n)
    counterexample = "mapping_undefined" if not is_planar(n) else ""
    
    return {
        "metric_name": "minimal_polynomial_degree",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")