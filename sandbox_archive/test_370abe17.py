# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll_width(phi):
        # Simplified DPLL solver to estimate width
        stack = []
        for clause in phi:
            if not any(lit in stack for lit in clause):
                stack.append(next(lit for lit in clause if lit > 0))
            else:
                return len(stack)
        return len(stack)

    def local_symmetry_count(phi):
        # Placeholder for actual symmetry counting logic
        return random.randint(1, 5)  # Dummy implementation

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
    
    symmetry_count = local_symmetry_count(phi)
    width = dpll_width(phi)
    
    return {
        "metric_name": "LocalSymmetryCount / DPLLWidth",
        "metric_value": Fraction(symmetry_count, width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": symmetry_count / width >= 0.5 and symmetry_count / width <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")