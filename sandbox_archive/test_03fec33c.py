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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = int(math.log2(len(f)))
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i * 2 + j] == 1:
                    A[i][j] = -1
                else:
                    A[i][j] = 1
        A[n][n] = len(f)
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if all(abs(A[i][j]) < 1e-9 for j in range(r)):
                continue
            r += 1
        return r
    
    def geometric_entropy(poly):
        n = len(poly)
        max_plus_poly = [max(poly[j], -poly[-j-1]) for j in range(n)]
        entropy = sum(math.log2(max_plus_poly[i] + 1) for i in range(n)) / n
        return entropy
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        protocol = []
        for i in range(2**n):
            if f[i] == 1:
                protocol.append(i)
        return rank(protocol)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = characteristic_polynomial(f)
        A = gaussian_elimination(A)
        rank_value = rank(A)
        ge_value = geometric_entropy(f)
        rcv_value = communication_complexity_rank_variance(f)
        
        results.append({
            "n": n,
            "ge_value": ge_value,
            "rcv_value": rcv_value
        })
    
    correlation_coefficient = sum((r["ge_value"] * r["rcv_value"] for r in results)) / len(results)
    mean_ge = sum(r["ge_value"] for r in results) / len(results)
    std_ge = math.sqrt(sum((r["ge_value"] - mean_ge)**2 for r in results) / len(results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.1,
        "counterexample": "" if abs(correlation_coefficient) > 0.1 else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 2**31 - 1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ge = sum(r["metric_value"] for r in results) / len(results)
    std_ge = math.sqrt(sum((r["metric_value"] - mean_ge)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ge} std={std_ge} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ge} std={std_ge} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")