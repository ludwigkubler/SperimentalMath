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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def young_tableau_algorithm(shape, elements):
    def insert(tableau, element):
        row = len(tableau)
        for r in range(row):
            if all(element >= tableau[r][c] for c in range(len(tableau[r]))):
                break
        else:
            r += 1
        new_row = sorted([*tableau[r], element])
        return [*tableau[:r], new_row, *tableau[r + 1:]]
    
    def generate_tableaux(elements):
        if not elements:
            yield []
        for i in range(len(elements)):
            for tableau in generate_tableaux(elements[:i] + elements[i+1:]):
                yield insert(tableau, elements[i])
    
    return list(generate_tableaux(elements))

def kronecker_coefficient(lam, mu):
    def hook_length_product(shape):
        result = 1
        for r in range(len(shape)):
            for c in range(len(shape[r])):
                h = shape[r][c] - c
                v = shape[r][c] - r
                d = min(r + 1, len(shape) - c)
                result *= (h * v * d) // ((r + 1) * (c + 1))
        return result
    
    def content_product(lam):
        result = 1
        for r in range(len(lam)):
            for c in range(len(lam[r])):
                result *= (lam[r][c] - c)
        return result
    
    n = sum(sum(row) for row in lam)
    m = sum(sum(row) for row in mu)
    if n != m:
        return 0
    sign = (-1) ** sum((len(lam) - i - 1) * (lam[i][j] - j) for i in range(len(lam)) for j in range(len(lam[i])))
    hlp_lam = hook_length_product(lam)
    hlp_mu = hook_length_product(mu)
    hlp_nu = hook_length_product([[lam[r][c] + mu[r][c] - c for c in range(max(len(lam[r]), len(mu[r]))) if c < len(lam[r]) and c < len(mu[r])] for r in range(max(len(lam), len(mu)))])
    cp_lam = content_product(lam)
    cp_mu = content_product(mu)
    cp_nu = content_product([[lam[r][c] + mu[r][c] - c for c in range(max(len(lam[r]), len(mu[r]))) if c < len(lam[r]) and c < len(mu[r])] for r in range(max(len(lam), len(mu)))])
    return sign * hlp_lam * hlp_mu // (hlp_nu * cp_lam * cp_mu)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = math.ceil(n / 2)
    m = random.randint(int(n ** 1.5), n - 1)
    
    perm_elements = list(range(1, n + 1))
    det_elements = list(range(1, m + 1))
    
    perm_tableaux = young_tableau_algorithm([(n,), (k,)], perm_elements)
    det_tableaux = young_tableau_algorithm([(m,), (k,)], det_elements)
    
    perm_coefficients = [kronecker_coefficient(lam, [(k,)]) for lam in perm_tableaux]
    det_coefficients = [kronecker_coefficient(lam, [(k,)]) for lam in det_tableaux]
    
    perm_sum_of_squares = sum(coef ** 2 for coef in perm_coefficients)
    det_sum_of_squares = sum(coef ** 2 for coef in det_coefficients)
    
    gap = perm_sum_of_squares - det_sum_of_squares
    conjecture_holds = gap >= 2 ** (n / 2)
    counterexample = "" if conjecture_holds else f"Gap {gap} < 2^{n/2}"
    
    return {
        "metric_name": "Kronecker_coefficient_gap",
        "metric_value": gap,
        "instances_tested": len(perm_tableaux),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gap = sum(res["metric_value"] for res in results) / len(results)
    std_gap = math.sqrt(sum((res["metric_value"] - mean_gap) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gap too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or no clear trend")