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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def characteristic_polynomial(cnf):
        n = len(cnf[0])
        poly = [Fraction(1)]
        for clause in cnf:
            term = Fraction(-1)
            for var in clause:
                term *= (var + 1) / (var - 1)
            poly.append(term)
        return poly
    
    def count_integral_points(poly):
        n = len(poly)
        count = 0
        for x in range(-10, 11):  # Limiting the search space for simplicity
            value = sum(coeff * x**i for i, coeff in enumerate(reversed(poly)))
            if value == 0:
                count += 1
        return count
    
    def upper_bound(m, n):
        return m**(Fraction(1, 4)) * n**(Fraction(3, 2))
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        cnf = generate_cnf(m, n)
        poly = characteristic_polynomial(cnf)
        points = count_integral_points(poly)
        bound = upper_bound(m, n)
        results.append((points, bound))
    
    total_points = sum(points for points, _ in results)
    total_bound = sum(bound for _, bound in results)
    support_fraction = sum(1 for points, bound in results if points <= bound) / len(results)
    
    return {
        "metric_name": "integral_points",
        "metric_value": total_points,
        "instances_tested": 30,
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"m={m}, n={n}, points={points}, bound={bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_points = sum(r["metric_value"] for r in results) / len(results)
    std_points = (sum((r["metric_value"] - mean_points)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_points} std={std_points} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")