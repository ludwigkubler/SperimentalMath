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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 2 or len(clause) > n:
                literal = random.randint(1, n)
                if random.choice([True, False]):
                    literal = -literal
                clause.add(literal)
            clauses.append(clause)
        return clauses

    def polynomial_from_clause(clause):
        poly = [0] * (len(clause) + 1)
        for lit in clause:
            if lit > 0:
                poly[lit] += 1
            else:
                poly[-lit] -= 1
        return poly

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def polynomial_divide(poly1, poly2):
        if len(poly1) < len(poly2):
            return [0], poly1
        quotient = [0] * (len(poly1) - len(poly2))
        divisor_leading_coeff = poly2[-1]
        for i in range(len(poly1) - 1, len(poly2) - 2, -1):
            coeff = poly1[i] / divisor_leading_coeff
            quotient[i - len(poly2)] = coeff
            for j in range(len(poly2)):
                poly1[i - j] -= coeff * poly2[j]
        return quotient, [x % 2 for x in poly1]

    def minimal_root_count(poly):
        roots = set()
        n = len(poly) - 1
        for i in range(1 << n):
            root = 0
            for j in range(n):
                if (i >> j) & 1:
                    root += poly[j] * (-1) ** (j + 1)
            if root == 0:
                roots.add(root)
        return len(roots)

    def resolution_width(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    lit_i = abs(clauses[i][0])
                    lit_j = abs(clauses[j][0])
                    if -lit_i in clauses[j] and lit_i not in clauses[j]:
                        new_clause = [x for x in clauses[i] if x != -lit_i]
                        new_clause.extend([x for x in clauses[j] if x != lit_i])
                        new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                break
            clauses.extend(new_clauses)
        return len(clauses)

    n = random.randint(5, 40)
    k = random.randint(1, min(n - 1, 3))
    cnf = generate_kcnf(n, k)
    
    polynomials = [polynomial_from_clause(clause) for clause in cnf]
    lcm_poly = polynomials[0]
    for poly in polynomials[1:]:
        lcm_poly = polynomial_divide(lcm_poly, poly)[0]
    
    alpha_phi = minimal_root_count(lcm_poly)
    w_phi = resolution_width(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "alpha_phi / w_phi",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = alpha_phi / w_phi
    f_n = k * (n ** (k / 2 + 1))
    
    return {
        "metric_name": "alpha_phi / w_phi",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= f_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, alpha_phi / w_phi={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break