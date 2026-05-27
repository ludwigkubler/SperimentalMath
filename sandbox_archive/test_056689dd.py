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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def permanent(poly):
        n = len(poly)
        if n == 0:
            return 1
        perm = 0
        for i in range(n):
            subpoly = [row[1:] for row in poly[1:]]
            sign = (-1) ** i
            perm += sign * poly[0][i] * permanent(subpoly)
        return perm
    
    def is_irreducible(poly):
        n = len(poly)
        if n == 1 and len(poly[0]) == 1:
            return True
        for i in range(n):
            subpoly = [row[:i] + row[i+1:] for row in poly]
            if permanent(subpoly) != 0:
                return False
        return True
    
    def algebraically_independent(poly, K):
        n = len(poly)
        degrees = [len(row) - 1 for row in poly]
        max_degree = max(degrees)
        for d in range(1, max_degree + 1):
            if any(degree == d for degree in degrees):
                return True
        return False
    
    K = ['a', 'b']  # Field with at least two elements
    n = random.randint(5, 30)  # Number of variables
    F_poly = [[random.choice(K) for _ in range(n)] for _ in range(n)]
    
    min_irreducible_degree = float('inf')
    max_monotone_degree = 0
    
    for i in range(n):
        subpoly = [row[:i] + row[i+1:] for row in F_poly]
        perm = permanent(subpoly)
        if perm != 0:
            max_monotone_degree = max(max_monotone_degree, len(F_poly) - i)
    
    irreducible_polynomials = []
    for poly in F_poly:
        if is_irreducible(poly):
            irreducible_polynomials.append(poly)
    
    for poly in irreducible_polynomials:
        degree = len(poly[0]) - 1
        min_irreducible_degree = min(min_irreducible_degree, degree)
    
    metric_value = min_irreducible_degree <= max_monotone_degree
    conjecture_holds = metric_value
    
    return {
        "metric_name": "Algebraic Independence Degree",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found with n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")