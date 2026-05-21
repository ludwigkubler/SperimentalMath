# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import permutations, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate enough clauses to ensure complexity
            clause = [random.randint(-n, n) for _ in range(3)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def polynomial_representation(clauses):
        poly = {}
        for clause in clauses:
            for lit in clause:
                if lit not in poly:
                    poly[lit] = 0
                poly[lit] += 1
        return poly
    
    def symmetric_group_orbits(poly, n):
        orbit_count = 0
        seen = set()
        
        for perm in permutations(range(1, n + 1)):
            permuted_poly = {perm[i-1]: poly[i] for i in range(1, n + 1)}
            key = tuple(sorted(permuted_poly.items()))
            if key not in seen:
                orbit_count += 1
                seen.add(key)
        
        return orbit_count
    
    def size(poly):
        return sum(poly.values())
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = polynomial_representation(clauses)
    orbit_count = symmetric_group_orbits(poly, n)
    
    metric_name = "orbit_count"
    metric_value = orbit_count
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if size(poly) >= 2**n / 2:
        if orbit_count > n / 2:
            conjecture_holds = True
        else:
            counterexample = "orbit_count <= n/2 for read-twice BP"
    elif orbit_count <= math.log(size(poly)):
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")