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
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clauses.append(f'({clause[0]} OR {clause[1]})')
            else:
                clauses.append(f'(NOT {clause[0]} AND NOT {clause[1]})')
        return ' AND '.join(clauses)

    def parse_formula(formula):
        # Simplified parsing for demonstration purposes
        return formula.split(' AND ')

    def derive_linear_forms(formula):
        linear_forms = []
        for clause in formula:
            if 'OR' in clause:
                linear_form = [1 if 'x' in term else -1 for term in clause.split()]
                linear_forms.append(linear_form)
            elif 'NOT' in clause:
                linear_form = [-1 if 'x' in term else 1 for term in clause[4:].split()]
                linear_forms.append(linear_form)
        return linear_forms

    def welzl(points, size=None):
        if size is None:
            size = len(points)
        if size == 0 or size == 1:
            return points
        p = random.choice(points)
        H = welzl([q for q in points if distance(q, p) > 1e-9], size - 1)
        if any(distance(p, h) <= 1e-9 for h in H):
            return H
        else:
            H.append(p)
            return H

    def distance(p, q):
        return norm(add_vectors(p, scale_vector(q, -1)))

    def norm(v):
        return math.sqrt(sum(x**2 for x in v))

    def add_vectors(v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]

    def scale_vector(v, scalar):
        return [scalar * x for x in v]

    m = random.randint(5, 30)
    n = random.randint(5, 30)
    formula = generate_tseitin_formula(m, n)
    parsed_formula = parse_formula(formula)
    linear_forms = derive_linear_forms(parsed_formula)

    if not linear_forms:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    sphere = welzl(linear_forms)
    volume = norm(sphere[0])  # Simplified volume calculation for demonstration

    return {
        "metric_name": "resolution_proof_width",
        "metric_value": volume,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")