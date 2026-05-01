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
from math import factorial, floor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def young_tableaux(n):
        if n == 0:
            return [[]]
        tableaux = []
        for i in range(1, n + 1):
            for subtableau in young_tableaux(n - i):
                tableaux.append([i] + subtableau)
        return tableaux
    
    def hook_length_formula(tableau):
        n = len(tableau)
        h = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                h[i][j] = (n - i) + (n - j) - 1
        det = 1
        for i in range(n):
            for j in range(n):
                det *= tableaux[i][j]
                det //= h[i][j]
        return det
    
    def littlewood_richardson_coefficient(λ, μ):
        if len(λ) != len(μ):
            return 0
        n = len(λ)
        a = [0] * (n + 1)
        b = [0] * (n + 1)
        c = [0] * (n + 1)
        d = [0] * (n + 1)
        for i in range(n):
            a[i] = λ[i]
            b[n - i - 1] = μ[i]
        for i in range(n + 1):
            c[i] = a[i] + b[i]
            d[i] = min(c[i], n - i)
        result = factorial(n) // (factorial(a[0]) * factorial(b[0]))
        for i in range(1, n + 1):
            result *= factorial(d[i] - d[i - 1]) // (factorial(a[i] - a[i - 1]) * factorial(b[i] - b[i - 1]))
        return result
    
    def permanent(poly):
        if len(poly) == 0:
            return 1
        n = len(poly)
        det = 0
        for i in range(n):
            subpoly = [row[:i] + row[i+1:] for row in poly[1:]]
            det += (-1) ** i * poly[0][i] * permanent(subpoly)
        return det
    
    def determinant(poly):
        if len(poly) == 0:
            return 1
        n = len(poly)
        det = 0
        for i in range(n):
            subpoly = [row[:i] + row[i+1:] for row in poly[1:]]
            det += (-1) ** i * poly[0][i] * determinant(subpoly)
        return det
    
    def tensor_power(poly, k):
        if k == 0:
            return [[1]]
        result = []
        for term in poly:
            new_term = [term[i] * term[j] for i in range(len(term)) for j in range(len(term))]
            result.append(new_term)
        return result
    
    def sum_littlewood_richardson(poly, λ):
        n = len(poly)
        k = floor(n ** 1.5)
        m = floor(n ** 0.5)
        det_poly = tensor_power([[i + 1 for i in range(m)]], k)
        perm_poly = tensor_power([[i + 1 for i in range(n)]], k)
        det_sum = sum(littlewood_richardson_coefficient(λ, μ) * determinant(det_poly) for μ in young_tableaux(k))
        perm_sum = sum(littlewood_richardson_coefficient(λ, μ) * permanent(perm_poly) for μ in young_tableaux(k))
        return det_sum / perm_sum
    
    n = random.randint(5, 40)
    λ = [random.randint(1, n) for _ in range(n)]
    ratio = sum_littlewood_richardson(λ, λ)
    
    conjecture_holds = ratio <= n ** (n - 1) and ratio >= n ** n
    counterexample = "" if conjecture_holds else f"Ratio {ratio} does not match expected bounds"
    
    return {
        "metric_name": "Littlewood-Richardson Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_ratio:.2f} std={std_ratio:.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)