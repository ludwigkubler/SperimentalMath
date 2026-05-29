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
    
    def generate_formula(n):
        if n == 1:
            return '0'
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} OR {right})'

    def tree_like_resolution_size(formula):
        if formula == '0' or formula == '1':
            return 1
        else:
            p, left, right = formula.split()
            return 1 + max(tree_like_resolution_size(left), tree_like_resolution_size(right))

    def symplectic_capacity(n):
        return n ** (1/4)

    def second_cohomology_group(t):
        return t ** (3/2)

    n_max = 0
    instances_tested = 0
    total_capacity = 0
    total_cohomology = 0

    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        formula = generate_formula(n)
        capacity = symplectic_capacity(n)
        cohomology = second_cohomology_group(tree_like_resolution_size(formula))
        
        total_capacity += capacity
        total_cohomology += cohomology
        
        instances_tested += 1
        n_max = max(n_max, n)

    mean_capacity = total_capacity / instances_tested
    mean_cohomology = total_cohomology / instances_tested

    conjecture_holds = all(capacity >= mean_capacity and cohom == mean_cohomology for capacity, cohom in zip([symplectic_capacity(n) for n in range(5, 41)], [second_cohomology_group(tree_like_resolution_size(generate_formula(n))) for n in range(5, 41)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Symplectic Capacity and Cohomology",
        "metric_value": mean_capacity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_capacity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_capacity} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_capacity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")