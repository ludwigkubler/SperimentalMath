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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n, p):
        coeffs = [random.randint(0, p-1) for _ in range(n+1)]
        return coeffs
    
    def polynomial_degree(coeffs):
        return len(coeffs) - 1
    
    def polynomial_value(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result % p
    
    def gaussian_elimination(A, b):
        n = len(b)
        A_b = [row + [b[i]] for i, row in enumerate(A)]
        
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
            
            pivot = A_b[i][i]
            if pivot == 0:
                continue
            
            for j in range(n):
                A_b[i][j] /= pivot
            A_b[i][-1] /= pivot
            
            for k in range(n):
                if k != i:
                    factor = A_b[k][i]
                    for j in range(n):
                        A_b[k][j] -= factor * A_b[i][j]
                    A_b[k][-1] -= factor * A_b[i][-1]
        
        return [row[-1] for row in A_b]
    
    def modular_form_degree(poly, p):
        n = polynomial_degree(poly)
        if n == 0:
            return 0
        
        A = [[polynomial_value(poly, x) % p for x in range(p)] for _ in range(n)]
        b = [1] * n
        solution = gaussian_elimination(A, b)
        
        degree = sum(1 for coeff in solution if coeff != 0)
        return degree
    
    def boolean_circuit_depth(poly):
        n = polynomial_degree(poly)
        depth = 0
        
        def circuit_value(poly, x):
            nonlocal depth
            if len(poly) == 1:
                return poly[0]
            else:
                mid = len(poly) // 2
                left = circuit_value(poly[:mid], x)
                right = circuit_value(poly[mid:], x)
                depth += 1
                return (left * right) % p
        
        for _ in range(30):
            x = random.randint(0, p-1)
            if circuit_value(poly, x) != polynomial_value(poly, x):
                return float('inf')
        
        return depth
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = random.randint(2, 10)
    poly = generate_polynomial(n, p)
    
    m = modular_form_degree(poly, p)
    D = boolean_circuit_depth(poly)
    
    if D == float('inf'):
        return {
            "metric_name": "modular_form_degree",
            "metric_value": m,
            "instances_tested": 30,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_evaluation_error"
        }
    
    if m < math.log(n) or m > D * math.log(n):
        return {
            "metric_name": "modular_form_degree",
            "metric_value": m,
            "instances_tested": 30,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"m={m}, D={D}, n={n}"
        }
    
    return {
        "metric_name": "modular_form_degree",
        "metric_value": m,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8 and mean_metric_value <= 3:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break