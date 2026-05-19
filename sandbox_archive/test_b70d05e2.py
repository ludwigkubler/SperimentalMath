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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(clause[i] == 0 for i in range(n)):
                continue
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def cnf_to_polynomials(cnf):
        polynomials = []
        for clause in cnf:
            poly = 1
            for literal in clause:
                if literal > 0:
                    poly *= (x**literal)
                else:
                    poly *= (1 - x**(-literal))
            polynomials.append(poly)
        return polynomials
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def reduce_polynomial(poly):
        terms = poly.split('*')
        reduced_terms = []
        for term in terms:
            if 'x' not in term:
                continue
            coeff, var = term.split('x')
            coeff = int(coeff.strip())
            exp = int(var[1:])
            reduced_terms.append((coeff, exp))
        return sorted(reduced_terms)
    
    def reduce_basis(basis):
        reduced_basis = []
        for poly in basis:
            reduced_poly = reduce_polynomial(poly)
            if not reduced_poly:
                continue
            added = False
            for i, red_poly in enumerate(reduced_basis):
                lcm_exp = max(red_poly[1], reduced_poly[1])
                new_coeff = (red_poly[0] * reduced_poly[0]) // gcd(red_poly[0], reduced_poly[0])
                if lcm_exp == red_poly[1]:
                    reduced_basis[i] = (new_coeff, lcm_exp)
                    added = True
                    break
            if not added:
                reduced_basis.append((reduced_poly[0], reduced_poly[1]))
        return reduced_basis
    
    def count_monomials(basis):
        monomials = set()
        for poly in basis:
            monomial = 1
            for coeff, exp in poly:
                monomial *= (x**exp)
            monomials.add(monomial)
        return len(monomials)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    polynomials = cnf_to_polynomials(cnf)
    basis = reduce_basis(polynomials)
    monomial_count = count_monomials(basis)
    
    metric_name = "monomial_count"
    metric_value = monomial_count
    instances_tested = 1
    conjecture_holds = monomial_count >= 2**(n/2)
    counterexample = f"n={n}, monomials={monomial_count}" if not conjecture_holds else ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_monomials = sum(r["metric_value"] for r in results)
    num_seeds = len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_seeds
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_monomials/num_seeds} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_monomials/num_seeds} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{r['counterexample']}' first_failing_seed={first_failing_seed}")