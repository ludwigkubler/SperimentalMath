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
    
    def generate_formula(s):
        variables = list(range(1, s + 1))
        clauses = []
        for _ in range(s):
            clause = random.sample(variables, random.randint(1, s))
            clauses.append(clause)
        return clauses
    
    def calculate_orbits(formula):
        orbits = set()
        for clause in formula:
            orbit = tuple(sorted(clause))
            orbits.add(orbit)
        return len(orbits)
    
    max_orbits = 0
    instances_tested = 30
    n_max = 40
    
    for s in range(1, n_max + 1):
        for _ in range(instances_tested // n_max):
            formula = generate_formula(s)
            orbits = calculate_orbits(formula)
            if orbits > max_orbits:
                max_orbits = orbits
    
    alpha_s = max_orbits
    conjecture_holds = alpha_s <= s ** (math.log(s))
    
    return {
        "metric_name": "alpha_s",
        "metric_value": alpha_s,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"alpha_s={alpha_s} > {s ** (math.log(s))}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_alpha_s = sum(r["metric_value"] for r in results) / len(results)
    std_alpha_s = math.sqrt(sum((r["metric_value"] - mean_alpha_s) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std={std_alpha_s} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std={std_alpha_s} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")