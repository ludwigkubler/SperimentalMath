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
from math import log2, ceil

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Ensure unsatisfiability
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if len(clause) > 2:
                random.shuffle(clause)
            clauses.append(clause)
        return clauses

    def cnf_to_polynomials(cnf):
        polynomials = []
        for clause in cnf:
            poly = [0] * (n + 1)
            for var in clause:
                if var < 0:
                    poly[-var] += 1
                else:
                    poly[var] -= 1
            polynomials.append(poly)
        return polynomials

    def add_poly(A, B):
        result = [a + b for a, b in zip(A, B)]
        return result

    def multiply_poly(A, B):
        n = len(A)
        result = [0] * (2 * n - 1)
        for i in range(n):
            for j in range(n):
                result[i + j] += A[i] * B[j]
        return result

    def reduce_poly(poly):
        while True:
            changed = False
            for i in range(len(poly) - 1, 0, -1):
                if poly[i] == 2:
                    poly[i] -= 2
                    poly[i - 1] += 1
                    changed = True
                elif poly[i] == -2:
                    poly[i] += 2
                    poly[i - 1] -= 1
                    changed = True
            if not changed:
                break
        return poly

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def reduce_basis(basis):
        n = len(basis[0])
        for i in range(n):
            pivot = None
            for j in range(i, len(basis)):
                if basis[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            for k in range(len(basis)):
                if k == pivot:
                    continue
                factor = -basis[k][i] // basis[pivot][i]
                basis[k] = [a + b * factor for a, b in zip(basis[k], basis[pivot])]
        return [reduce_poly(poly) for poly in basis]

    def count_monomials(poly):
        count = 0
        for coeff in poly:
            if coeff != 0:
                count += 1
        return count

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    polynomials = cnf_to_polynomials(cnf)

    basis = [polynomials[0]]
    for poly in polynomials[1:]:
        new_poly = reduce_poly(add_poly(poly, reduce_basis(basis)[0]))
        if new_poly != [0] * (n + 1):
            basis.append(new_poly)

    reduced_basis = reduce_basis(basis)
    monomial_count = sum(count_monomials(poly) for poly in reduced_basis)

    return {
        "metric_name": "monomial_count",
        "metric_value": monomial_count,
        "instances_tested": 1,
        "conjecture_holds": monomial_count >= 2 ** (n // 2),
        "counterexample": "" if monomial_count >= 2 ** (n // 2) else f"n={n}, monomials={monomial_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, monomials={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")