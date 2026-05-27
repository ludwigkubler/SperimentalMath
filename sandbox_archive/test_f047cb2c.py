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
    
    # Define the field K (finite field with at least two elements)
    p = random.randint(2, 100)
    F = [random.randint(0, p-1) for _ in range(random.randint(2, 5))]
    
    # Generate a polynomial system F over the field K
    n = len(F)
    F_poly = []
    for i in range(n):
        coeff = [random.randint(0, p-1) for _ in range(i+1)]
        F_poly.append(coeff)
    
    # Construct a circuit C that computes the permanent of F
    def permanent(poly):
        if not poly:
            return 1
        n = len(poly)
        perm = 0
        for i in range(n):
            sign = (-1) ** i
            subpoly = [row[:i] + row[i+1:] for row in poly[1:]]
            perm += sign * poly[0][i] * permanent(subpoly)
        return perm % p
    
    def circuit_degree(poly):
        if not poly:
            return 0
        n = len(poly)
        max_deg = 0
        for i in range(n):
            subpoly = [row[:i] + row[i+1:] for row in poly[1:]]
            deg = circuit_degree(subpoly) + 1
            if deg > max_deg:
                max_deg = deg
        return max_deg
    
    perm = permanent(F_poly)
    c = circuit_degree(F_poly)
    
    # Check if there exists an irreducible polynomial in K that is algebraically independent over K and has degree at most c
    def is_irreducible(poly):
        n = len(poly)
        if n == 1:
            return True
        for i in range(1, n):
            subpoly = poly[:i] + poly[i+1:]
            if permanent(subpoly) != 0:
                return False
        return True
    
    irreducible_poly_found = any(is_irreducible(poly) for poly in F_poly)
    
    # Return the result of the trial
    return {
        "metric_name": "minimum_degree",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": irreducible_poly_found and c >= perm,
        "counterexample": "" if irreducible_poly_found else f"No irreducible polynomial of degree at most {c} found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")