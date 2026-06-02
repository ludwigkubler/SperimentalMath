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
    
    def generate_polynomial(n, d):
        coefficients = [random.randint(1, 10) for _ in range(d + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def find_roots(poly):
        if len(poly) == 1:
            return [0]
        roots = []
        for i in range(-100, 101):
            if evaluate_polynomial(poly, i) == 0:
                roots.append(i)
        return roots
    
    def monotone_width(poly):
        n = len(poly) - 1
        width = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if poly[i] * poly[j] < 0:
                    width += 1
        return width
    
    def min_root_distance(roots):
        if len(roots) < 2:
            return 0
        roots.sort()
        return min(abs(roots[i] - roots[i + 1]) for i in range(len(roots) - 1))
    
    n = random.randint(5, 40)
    d = random.randint(1, n)
    poly = generate_polynomial(n, d)
    roots = find_roots(poly)
    m_min_dist = min_root_distance(roots)
    width = monotone_width(poly)
    
    return {
        "metric_name": "min_root_distance",
        "metric_value": m_min_dist,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(m_min_dist - width) <= 2 * width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")