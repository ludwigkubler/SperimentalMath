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
    
    def is_3sat_clause(clause):
        return len(clause) == 3 and all(x in {'x', 'y', 'z'} for x in clause)
    
    def generate_random_3sat(n, m):
        clauses = []
        variables = ['x', 'y', 'z']
        while len(clauses) < m:
            clause = [random.choice(variables) + random.choice(['', "'"]) for _ in range(3)]
            if is_3sat_clause(clause):
                clauses.append(clause)
        return clauses
    
    def polynomial_from_clause(clause):
        x, y, z = 'x', 'y', 'z'
        clause_poly = 1
        for var in clause:
            if var[0] == 'x':
                coeff = -1 if var[1] == "'" else 1
                clause_poly *= (coeff * x + int(var[1] != "'"))
            elif var[0] == 'y':
                coeff = -1 if var[1] == "'" else 1
                clause_poly *= (coeff * y + int(var[1] != "'"))
            elif var[0] == 'z':
                coeff = -1 if var[1] == "'" else 1
                clause_poly *= (coeff * z + int(var[1] != "'"))
        return clause_poly
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def s_polynomial(f, g):
        m1, m2 = f[0], g[0]
        if m1 < m2:
            f, g = g, f
            m1, m2 = m2, m1
        lcm_monomial = 1
        for i in range(len(m1)):
            lcm_monomial *= lcm(m1[i], m2[i])
        s_poly = [0] * len(f)
        for i in range(len(f)):
            s_poly[i] = (lcm_monomial // m1[i]) * f[i]
            if m1[i] > m2[i]:
                s_poly[i] -= (lcm_monomial // m2[i]) * g[i]
        return s_poly
    
    def reduce_polynomial(poly, monomials):
        for i in range(len(monomials)):
            while poly[0] >= monomials[i][0]:
                coeff = poly[1] / monomials[i][1]
                poly[1] -= coeff * monomials[i][2]
                poly[0] -= 1
        return poly
    
    def buchberger_algorithm(poly_system):
        S_polynomials = []
        for i in range(len(poly_system)):
            for j in range(i + 1, len(poly_system)):
                s_poly = s_polynomial(poly_system[i], poly_system[j])
                if any(s_poly[k] != 0 for k in range(len(s_poly))):
                    S_polynomials.append((s_poly[0], s_poly[1]))
        return S_polynomials
    
    def count_spolynomials(poly_system):
        S_polynomials = buchberger_algorithm(poly_system)
        return len(S_polynomials)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_random_3sat(n, m)
    poly_system = [polynomial_from_clause(clause) for clause in clauses]
    
    s_poly_count = count_spolynomials(poly_system)
    
    expected_s_poly_count = math.ceil(2**(n/2))
    
    return {
        "metric_name": "S-polynomial reductions",
        "metric_value": s_poly_count,
        "instances_tested": 1,
        "conjecture_holds": abs(s_poly_count - expected_s_poly_count) <= 0.1 * expected_s_poly_count,
        "counterexample": "" if abs(s_poly_count - expected_s_poly_count) <= 0.1 * expected_s_poly_count else f"Expected {expected_s_poly_count}, got {s_poly_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_s_poly_count = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_s_poly_count)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_s_poly_count} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")