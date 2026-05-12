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

def generate_random_3sat(n):
    clauses = []
    for _ in range(2**n):
        clause = [random.randint(0, n-1) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def polynomials_to_gf2_polys(n, clauses):
    polys = []
    for clause in clauses:
        poly = 1
        for var in clause:
            poly *= (1 + x[var])
        polys.append(poly % 2)
    return polys

def groebner_basis(polys):
    # Simple implementation of Groebner basis using Buchberger's algorithm
    def s_polynomial(f, g):
        deg_f = max(len(p) for p in f if p != 0)
        deg_g = max(len(p) for p in g if p != 0)
        lcm_deg = deg_f + deg_g
        lead_f = next((p for p in f if len(p) == deg_f), 0)
        lead_g = next((p for p in g if len(p) == deg_g), 0)
        return (lcm_deg - deg_f) * lead_f - (lcm_deg - deg_g) * lead_g

    basis = list(polys)
    while True:
        new_basis = []
        for i in range(len(basis)):
            for j in range(i+1, len(basis)):
                spoly = s_polynomial(basis[i], basis[j])
                if spoly != 0:
                    reduced_spoly = reduce_poly(spoly, basis)
                    if reduced_spoly != 0:
                        new_basis.append(reduced_spoly)
        if set(new_basis) == set(basis):
            break
        basis.extend(new_basis)
    return basis

def reduce_poly(poly, basis):
    for b in basis:
        while poly % b == 0:
            poly = poly // b
    return poly

def sos_refutation_degree(groebner_basis):
    # Simple implementation of SOS refutation degree
    max_deg = 0
    for p in groebner_basis:
        if len(p) > max_deg:
            max_deg = len(p)
    return max_deg

def irreducible_components(groebner_basis):
    # Simple implementation of irreducible components using factorization
    def is_irreducible(poly):
        for i in range(1, len(poly)):
            if poly % (poly - x[i]) == 0:
                return False
        return True

    components = []
    for p in groebner_basis:
        if is_irreducible(p):
            components.append(p)
    return components

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_random_3sat(n)
    polys = polynomials_to_gf2_polys(n, clauses)
    groebner_basis = groebner_basis(polys)
    sos_degree = sos_refutation_degree(groebner_basis)
    components = irreducible_components(groebner_basis)
    component_count = len(components)
    if sos_degree == 0:
        return {
            "metric_name": "component_count",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sos_degree_undefined"
        }
    metric_value = component_count / (sos_degree ** 2)
    conjecture_holds = abs(metric_value - 1/(sos_degree**2)) < 0.1
    counterexample = "" if conjecture_holds else f"component_count={component_count}, sos_degree={sos_degree}"
    return {
        "metric_name": "component_count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"component_count_vs_sos_degree\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")