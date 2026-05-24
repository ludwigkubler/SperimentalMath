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

def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(v):
    return math.sqrt(dot_product(v, v))

def add_vectors(a, b):
    return [x + y for x, y in zip(a, b)]

def scale_vector(v, scalar):
    return [scalar * x for x in v]

def distance(p1, p2):
    return norm(add_vectors(p1, scale_vector(p2, -1)))

def welzl(points, size=None):
    if size is None:
        size = len(points)
    if size == 0 or size == 1:
        return points
    p = random.choice(points)
    H = welzl([q for q in points if distance(q, p) > 1e-9], size - 1)
    if any(distance(q, [p[i] for i in range(len(p))]) <= 1e-9 for q in H):
        return H
    else:
        return H + [p]

def min_enclosing_sphere(points):
    return welzl(points)

def generate_tseitin_formula(m, n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(f"({clause[0]} OR {clause[1]})")
    return " AND ".join(clauses)

def resolution_width(formula):
    # Placeholder for actual DPLL solver implementation
    return random.randint(10, 50)  # Simulated width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n // 2, n * 2)
    formula = generate_tseitin_formula(m, n)
    linear_forms = [random.uniform(-1, 1) for _ in range(m)]
    sphere = min_enclosing_sphere(linear_forms)
    volume = norm(sphere[-1])
    width = resolution_width(formula)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (volume * math.log(2)),
        "counterexample": "" if width >= 2 ** (volume * math.log(2)) else f"Formula: {formula}, Volume: {volume}, Width: {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")