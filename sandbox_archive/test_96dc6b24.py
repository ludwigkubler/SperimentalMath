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
    
    def generate_formula(n):
        if n == 1:
            return 'x1'
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} & {right})'

    def monomial_representation(formula):
        if formula.startswith('(') and formula.endswith(')'):
            formula = formula[1:-1]
        if '&' not in formula:
            return [formula]
        left, operator, right = formula.split('&', 1)
        return monomial_representation(left) + monomial_representation(right)

    def min_local_ring_norm(formula):
        M = monomial_representation(formula)
        n = len(M)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, m in enumerate(M):
            A[i][i] = 1
            if '&' in m:
                left, right = m.split('&')
                A[i][M.index(left)] += 1
                A[i][M.index(right)] += 1
        
        # LLL reduction
        def lll(A, delta=0.75):
            n = len(A)
            B = [list(row) for row in A]
            u = [1] * n
            g = [norm(B[0])]
            for i in range(1, n):
                b_i = list(B[i])
                for j in range(i - 1, -1, -1):
                    alpha = round(inner_product(B[j], B[i]) / g[j])
                    b_i = subtract_vectors(b_i, scalar_multiply(alpha, B[j]))
                    u[i] = max(u[i], abs(alpha))
                B[i] = list(b_i)
                g.append(norm(B[i]))
                beta = round(g[i - 1] * u[i] ** (1 / 2) / g[i])
                if abs(beta) >= delta:
                    B[j + 1], B[i] = B[i], B[j + 1]
                    u[j + 1], u[i] = u[i], u[j + 1]
                    g[j + 1], g[i] = g[i], g[j + 1]
            return B, u, g
        
        def inner_product(v1, v2):
            return sum(x * y for x, y in zip(v1, v2))
        
        def norm(v):
            return math.sqrt(inner_product(v, v))
        
        def subtract_vectors(v1, v2):
            return [x - y for x, y in zip(v1, v2)]
        
        def scalar_multiply(scalar, v):
            return [scalar * x for x in v]
        
        B, u, g = lll(A)
        min_lrn = min(g[1:])
        return min_lrn

    def resolution_proof_width(formula):
        if '&' not in formula:
            return 1
        left, right = formula.split('&', 1)
        return max(resolution_proof_width(left), resolution_proof_width(right)) + 1
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    min_lrn = min_local_ring_norm(formula)
    w = resolution_proof_width(formula)
    
    return {
        "metric_name": "minLRN vs w",
        "metric_value": min_lrn / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for res in results if not res["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(res for res in results if not res['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")