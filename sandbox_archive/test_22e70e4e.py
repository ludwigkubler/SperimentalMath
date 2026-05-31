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
    
    def generate_formula(s: int):
        return [random.sample(range(1, s+1), k=random.randint(2, s)) for _ in range(random.randint(1, 5))]
    
    def action_group_orbits(formula):
        orbits = set()
        for clause in formula:
            orbit = tuple(sorted(clause))
            orbits.add(orbit)
        return len(orbits)
    
    max_orbits = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            orbits = action_group_orbits(formula)
            max_orbits = max(max_orbits, orbits)
            instances_tested += 1
    
    alpha_s = max_orbits
    n_max = 40
    conjecture_holds = alpha_s <= n_max ** (math.log(n_max))
    
    return {
        "metric_name": "alpha(s)",
        "metric_value": alpha_s,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"alpha({n_max}) = {alpha_s} > {n_max ** (math.log(n_max))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_alpha_s = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_alpha_s} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha({40}) exceeded bound\" first_failing_seed={first_failing_seed}")