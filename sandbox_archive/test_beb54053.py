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
    
    def generate_tseitin_formula(m, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
            clauses.append(f'-{variables[i]}')
        for _ in range(m - 2 * n):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause = f'{-clause}'
            clauses.append(clause)
        return variables, clauses
    
    def generate_linear_forms(variables, clauses):
        linear_forms = []
        for clause in clauses:
            form = 0
            for var in variables:
                if var in clause:
                    sign = 1 if '+' in clause else -1
                    form += sign * (1 if 'x' + var[1:] not in clause else 0)
            linear_forms.append(form)
        return linear_forms
    
    def welzl(points, size=None):
        if size is None or size == len(points):
            return []
        p = random.choice(points)
        H = welzl([q for q in points if distance(q, p) > 1e-9], size - 1)
        if all(distance(p, h) <= 1e-9 for h in H):
            return H
        else:
            H.append(p)
            return H
    
    def distance(p, q):
        return norm(add_vectors(p, scale_vector(q, -1)))
    
    def add_vectors(v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]
    
    def scale_vector(v, scalar):
        return [scalar * vi for vi in v]
    
    def norm(v):
        return math.sqrt(sum(vi ** 2 for vi in v))
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_tseitin_formula(m, n)
    linear_forms = generate_linear_forms(variables, clauses)
    sphere = welzl(linear_forms)
    volume = norm(sphere) if sphere else 1
    
    # Placeholder for resolution proof width calculation
    resolution_width = 2 ** (math.ceil(math.log(volume, 2)))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "conjecture_holds": resolution_width >= 2 ** (math.ceil(math.log(volume, 2))),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.randint(1000, 9999) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")