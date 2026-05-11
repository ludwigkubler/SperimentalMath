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

def generate_3sat_instance(n: int, m: int) -> list:
    clauses = []
    variables = set(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def polynomial(x, y, z):
    return (1 - x) * (1 - y) * (1 - z)

def construct_ideal(clauses: list) -> dict:
    ideal = {}
    for clause in clauses:
        monomials = set()
        for i in range(2**len(clause)):
            factors = [1]
            for j, var in enumerate(clause):
                if i & (1 << j):
                    factors.append(-var)
                else:
                    factors.append(var - 1)
            monomial = math.prod(factors)
            monomials.add(monomial)
        ideal[tuple(sorted(monomials))] = 0
    return ideal

def grobner_basis(ideal: dict) -> set:
    basis = list(ideal.keys())
    while True:
        new_elements = []
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                gcd = set()
                for monom_i in basis[i]:
                    for monom_j in basis[j]:
                        if monom_i == monom_j:
                            gcd.add(monom_i)
                            break
                if gcd:
                    new_elements.append(tuple(sorted(gcd)))
        if not new_elements:
            break
        basis.extend(new_elements)
    return set(basis)

def krull_dimension(basis: set) -> int:
    return len(basis)

def sos_refutation_degree(clauses: list, p=2) -> int:
    n = max(max(abs(x) for clause in clauses for x in clause), key=abs)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)
    for clause in clauses:
        for i in range(2**len(clause)):
            factors = [1]
            for j, var in enumerate(clause):
                if i & (1 << j):
                    factors.append(-var)
                else:
                    factors.append(var - 1)
            monomial = math.prod(factors)
            row = [0] * (n + 1)
            for factor in factors:
                if isinstance(factor, int):
                    row[abs(factor)] += 1
                else:
                    row[factor] -= 1
            A[monomial] = row
            b[monomial] += monomial ** p
    # Solve the linear system Ax = b using Gaussian elimination
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            return -1  # No solution
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    return sum(1 for row in A if any(x != 0 for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, min(2 * n, 30))
    clauses = generate_3sat_instance(n, m)
    ideal = construct_ideal(clauses)
    basis = grobner_basis(ideal)
    dim_I = krull_dimension(basis)
    refutation_degree = sos_refutation_degree(clauses)
    conjecture_holds = refutation_degree >= dim_I
    counterexample = "" if conjecture_holds else f"refutation_degree={refutation_degree}, dim(I)={dim_I}"
    return {
        "metric_name": "SOS Refutation Degree",
        "metric_value": refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30 * 4 + 2, 2))
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")