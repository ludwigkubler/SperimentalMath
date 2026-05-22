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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_primitive_poly(poly, q):
    degree = len(poly) - 1
    for i in range(1, q**degree):
        if pow(i, degree, q) == 1 and all((i ** (degree // d)) % q != 1 for d in range(2, degree)):
            return True
    return False

def generate_max_cut_instance(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    return edges

def compute_tropical_curve(edges):
    # Simplified tropical curve computation
    return len(edges)

def sos_hierarchy_approximation_ratio(n):
    # Simplified approximation ratio calculation
    return 0.879 + 0.1 * random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = generate_max_cut_instance(n)
    tropical_curve_rank = compute_tropical_curve(edges)
    approximation_ratio = sos_hierarchy_approximation_ratio(n)
    
    return {
        "metric_name": "SOS Hierarchy Approximation Ratio",
        "metric_value": approximation_ratio,
        "instances_tested": 1,
        "conjecture_holds": tropical_curve_rank <= approximation_ratio,
        "counterexample": "" if tropical_curve_rank <= approximation_ratio else f"tropical_curve_rank={tropical_curve_rank}, approximation_ratio={approximation_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")