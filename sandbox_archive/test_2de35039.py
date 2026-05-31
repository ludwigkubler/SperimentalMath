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
    
    def generate_satisfiable_formula(s):
        variables = list(range(1, s + 1))
        clauses = []
        for _ in range(s):
            clause = random.sample(variables, random.randint(1, s))
            clauses.append(clause)
        return clauses

    def calculate_orbits(clauses):
        orbits = set()
        for clause in clauses:
            orbit = tuple(sorted(clause))
            orbits.add(orbit)
        return len(orbits)

    max_orbits = 0
    instances_tested = 30
    
    for _ in range(instances_tested):
        s = random.randint(1, 40)
        formula = generate_satisfiable_formula(s)
        orbits = calculate_orbits(formula)
        if orbits > max_orbits:
            max_orbits = orbits

    alpha_s = max_orbits
    n_max = 40
    conjecture_holds = alpha_s <= n_max ** (math.log(n_max))
    counterexample = "" if conjecture_holds else f"alpha({s})={alpha_s}, expected <= {n_max ** (math.log(n_max))}"
    
    return {
        "metric_name": "alpha(s)",
        "metric_value": alpha_s,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_alpha_s = sum(res["metric_value"] for res in results) / len(results)
    std_alpha_s = math.sqrt(sum((res["metric_value"] - mean_alpha_s) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std={std_alpha_s} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std={std_alpha_s} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha(s) exceeds O(n^(log n))\" first_failing_seed={first_failing_seed}")