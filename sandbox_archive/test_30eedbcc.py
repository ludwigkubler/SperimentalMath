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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    return sum(1 for row in A if any(row))

def generate_max_cut_instance(n):
    variables = [f'x{i}' for i in range(n)]
    terms = []
    for i in range(n):
        for j in range(i + 1, n):
            terms.append((Fraction(1), [(i, 1), (j, 1)]))
    return variables, terms

def evaluate_polynomial(p, x_values):
    result = Fraction(0)
    for coeffs, exponents in p:
        term = Fraction(1)
        for var, exp in zip(exponents, x_values):
            term *= x_values[var] ** exp
        result += coeffs * term
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, terms = generate_max_cut_instance(n)
    d = len(terms[0][1])
    
    # Evaluate polynomial at random points
    x_values = {var: Fraction(random.randint(-10, 10)) for var in variables}
    p_value = evaluate_polynomial(terms, [x_values[var] for var in variables])
    
    M_p = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for coeffs, exponents in terms:
        for i in range(n):
            for j in range(n):
                term = Fraction(1)
                for var, exp in zip(exponents, [x_values[variables[i]], x_values[variables[j]]]):
                    term *= variables[var] ** exp
                M_p[i][j] += coeffs * term
    
    rank_M_p = rank(M_p)
    
    if rank_M_p < d * math.log(n) ** 2:
        ratio = p_value / (n * (n - 1) // 2)
        if ratio > Fraction(878, 1000):
            return {
                "metric_name": "rank",
                "metric_value": rank_M_p,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
        else:
            return {
                "metric_name": "rank",
                "metric_value": rank_M_p,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Approximation ratio {ratio} is not worse than 0.878"
            }
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank_M_p,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        print(f"RESULT: FALSIFIED counterexample='approximation_ratio_not_worse_than_0.878' first_failing_seed={first_failing_seed}")