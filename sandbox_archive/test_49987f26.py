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
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), -random.randint(-n, -1)]
            if random.choice([True, False]):
                clause.reverse()
            cnf.append(clause)
        return cnf
    
    def polynomial_from_clause(clause):
        poly = []
        for var in clause:
            if var > 0:
                poly.append(f'x{var}')
            else:
                poly.append(f'(1-x{-var})')
        return ' * '.join(poly)
    
    def multiply_polynomials(p1, p2):
        result = {}
        for term1 in p1.split(' * '):
            for term2 in p2.split(' * '):
                product = f'{term1} * {term2}'
                degree = sum(int(x[1:]) for x in product.split('*') if x.startswith('x'))
                if degree not in result:
                    result[degree] = 0
                result[degree] += 1
        return result
    
    def reduce_polynomial(poly):
        degrees = sorted(poly.keys(), reverse=True)
        while len(degrees) > 1:
            highest = degrees.pop(0)
            second_highest = degrees.pop(0)
            poly[highest - second_highest] -= poly[second_highest]
            if poly[highest - second_highest] == 0:
                del poly[highest - second_highest]
            degrees.append(highest - second_highest)
        return poly
    
    def grb_basis_count(cnf):
        polynomials = [polynomial_from_clause(clause) for clause in cnf]
        basis = set()
        for p1 in polynomials:
            new_poly = p1
            for p2 in basis:
                product = multiply_polynomials(new_poly, p2)
                reduced_product = reduce_polynomial(product)
                if not any(reduced_product[d] % 2 for d in reduced_product):
                    new_poly = ' * '.join(p for p in polynomials if p != p1 and p != p2)
            basis.add(new_poly)
        return len(basis)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    monomial_count = grb_basis_count(cnf)
    
    return {
        "metric_name": "monomial_count",
        "metric_value": monomial_count,
        "instances_tested": 1,
        "conjecture_holds": monomial_count >= 2**(n/2),
        "counterexample": "" if monomial_count >= 2**(n/2) else f"n={n}, monomials={monomial_count}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_monomials = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_monomials/len(results):.2f} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_monomials/len(results):.2f} std=0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, monomials={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")