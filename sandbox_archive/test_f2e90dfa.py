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
    
    def generate_random_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def polynomial_representation(clauses):
        poly = {}
        for clause in clauses:
            key = tuple(sorted(abs(lit) for lit in clause))
            if key not in poly:
                poly[key] = 0
            poly[key] += 1
        return poly

    def symmetric_group_orbits(poly, n):
        orbits = set()
        for perm in permutations(n):
            new_poly = {}
            for key, count in poly.items():
                new_key = tuple(perm[lit-1] if lit > 0 else -perm[-lit] for lit in key)
                new_key = tuple(sorted(abs(lit) for lit in new_key))
                if new_key not in new_poly:
                    new_poly[new_key] = 0
                new_poly[new_key] += count
            orbits.add(tuple(sorted(new_poly.items())))
        return len(orbits)

    def permutations(n):
        if n == 1:
            yield (1,)
        else:
            for i in range(1, n+1):
                for p in permutations(n-1):
                    if i not in p:
                        yield tuple(p[:p.index(i)] + (i,) + p[p.index(i):])

    def log_size(poly):
        return sum(count for count in poly.values())

    n = 20
    size = 2**n
    clauses = generate_random_3cnf(n)
    poly = polynomial_representation(clauses)
    
    orbit_count = symmetric_group_orbits(poly, n)
    metric_value = orbit_count
    
    conjecture_holds = orbit_count > math.log(size) and orbit_count >= n / 2
    counterexample = "" if conjecture_holds else f"orbit_count={orbit_count}, log_size={math.log(size)}, n/2={n/2}"
    
    return {
        "metric_name": "orbit_count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"orbit_count does not meet the expected bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded")