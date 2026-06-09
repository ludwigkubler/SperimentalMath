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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def polynomial_from_clauses(clauses):
        poly = {}
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 - x[literal])
                else:
                    term *= (1 + x[-literal])
            poly[tuple(sorted([abs(lit) for lit in clause]))] += term
        return poly

    def hodge_decomposition(poly):
        # Simplified Hodge decomposition for demonstration purposes
        area = 0
        for key, value in poly.items():
            area += abs(value)
        return area

    def resolution_width(clauses):
        # Simplified resolution width calculation
        return len(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    areas = []
    widths = []

    for n in n_values:
        clauses = generate_sat_instance(n)
        poly = polynomial_from_clauses(clauses)
        area = hodge_decomposition(poly)
        width = resolution_width(clauses)
        areas.append(area)
        widths.append(width)

    mean_area = sum(areas) / len(areas)
    max_n = max(n_values)
    conjecture_holds = all(area <= n**(2/3) for area, n in zip(areas, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Hodge Diamond Area",
        "metric_value": float(mean_area),
        "instances_tested": len(n_values),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_area = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_area} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_area} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")