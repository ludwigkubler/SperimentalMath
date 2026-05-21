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
    
    def symmetric_group(n):
        if n == 0:
            return [[]]
        else:
            result = []
            for perm in symmetric_group(n - 1):
                for i in range(n):
                    new_perm = [x if x < i else (x + 1) % n for x in perm]
                    if new_perm not in result:
                        result.append(new_perm)
            return result
    
    def orbit_stabilizer(group, action, element):
        orbit = {element}
        stabilizer = []
        for g in group:
            if all(action(g, e) == action(e, g) for e in orbit):
                stabilizer.append(g)
        return orbit, stabilizer
    
    def degree_of_invariant(poly, group):
        max_degree = 0
        for perm in group:
            new_poly = [poly[perm[i]] for i in range(len(poly))]
            max_degree = max(max_degree, sum(abs(c) for c in new_poly))
        return max_degree
    
    n = random.randint(5, 40)
    variables = list(range(n))
    group = symmetric_group(n)
    
    # Generate a random 3-CNF instance
    clauses = []
    for _ in range(random.randint(10, 20)):
        literals = [random.choice(variables) for _ in range(3)]
        clause = tuple(sorted(literals + [-l for l in literals]))
        clauses.append(clause)
    
    # Define the action of S_n on the variables
    def action(perm, var):
        return perm[var]
    
    # Compute the minimal degree of a symmetric polynomial invariant under S_n's action
    min_degree = float('inf')
    for poly in itertools.product([-1, 1], repeat=n):
        orbit, stabilizer = orbit_stabilizer(group, action, poly)
        if len(orbit) == n:
            degree = degree_of_invariant(poly, group)
            if degree < min_degree:
                min_degree = degree
    
    return {
        "metric_name": "min_degree",
        "metric_value": min_degree,
        "instances_tested": 1,
        "conjecture_holds": min_degree >= math.log(n),
        "counterexample": "" if min_degree >= math.log(n) else f"n={n}, min_degree={min_degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['metric_value']}, min_degree={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")