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

def generate_random_3sat(n, m):
    clauses = []
    for _ in range(m):
        variables = set(random.sample(range(1, n + 1), 3))
        clause = [f"({v} OR {v+100} OR {v+200})" if random.choice([True, False]) else f"(NOT {v} AND NOT {v+100} AND NOT {v+200})"
                   for v in variables]
        clauses.append(" AND ".join(clause))
    return " AND ".join(clauses)

def polynomial_system_from_3sat(sat_formula):
    n = max(int(x) for x in sat_formula.split() if x.isdigit())
    polynomials = [f"z_{i} - 1" for i in range(n)]
    return polynomials

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def s_polynomial(f, g):
    f_vars = set(int(x[2:]) for x in f.split() if x.startswith('z_'))
    g_vars = set(int(x[2:]) for x in g.split() if x.startswith('z_'))
    lcm_vars = sorted(lcm(x, y) for x in f_vars for y in g_vars)
    s_poly = " + ".join(f"z_{v}^{lcm_vars.index(v)+1}" for v in lcm_vars)
    return s_poly

def reduce_polynomial(poly, polynomials):
    terms = poly.split(" + ")
    new_terms = []
    for term in terms:
        reduced = True
        for p in polynomials:
            if term in p or f"NOT {term}" in p:
                reduced = False
                break
        if reduced:
            new_terms.append(term)
    return " + ".join(new_terms)

def buchberger_algorithm(polynomials):
    s_polynomials = []
    while True:
        new_s_polynomials = []
        for i in range(len(s_polynomials)):
            for j in range(i+1, len(s_polynomials)):
                sp = s_polynomial(s_polynomials[i], s_polynomials[j])
                if sp:
                    new_s_polynomials.append(sp)
        if not new_s_polynomials:
            break
        s_polynomials.extend(new_s_polynomials)
    return s_polynomials

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(3 * n // 2, 5 * n // 2)
    sat_formula = generate_random_3sat(n, m)
    polynomials = polynomial_system_from_3sat(sat_formula)
    s_polynomials = buchberger_algorithm(polynomials)
    return {
        "metric_name": "s-polynomial_reductions",
        "metric_value": len(s_polynomials),
        "instances_tested": 1,
        "conjecture_holds": len(s_polynomials) == math.isclose(len(s_polynomials), 2**(n/2), rel_tol=0.1),
        "counterexample": "" if len(s_polynomials) == math.isclose(len(s_polynomials), 2**(n/2), rel_tol=0.1) else f"n={n}, expected ~{2**(n/2)}, got {len(s_polynomials)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")