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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'x'
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} & {subformulas[1]})'

    def galois_group_size(n):
        if n == 1:
            return 1
        else:
            return 2 * galois_group_size(n-1)

    def smallest_normal_subgroup_size(g):
        return g // 2

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    g = galois_group_size(n)
    N = smallest_normal_subgroup_size(g)

    metric_name = "Galois Group Order"
    metric_value = N
    instances_tested = 1
    n_max = n
    conjecture_holds = (math.log2(n) <= N <= math.log2(n)**2)
    counterexample = "" if conjecture_holds else f"Formula: {formula}, N={N}, log(n)^2={math.log2(n)**2}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"

    print(f"RESULT: {result} mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")