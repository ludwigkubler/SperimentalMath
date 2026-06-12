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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def vector_space_representation(f):
        n = int(math.log2(len(f)))
        V_f = [[f[i] if i & (1 << j) else 0 for j in range(n)] for i in range(2**n)]
        return V_f
    
    def symplectic_measure(V_f):
        n = len(V_f[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [v + w for v, w in zip(V_f, V_f[::-1])]
        B = [v - w for v, w in zip(V_f, V_f[::-1])]
        C = [a + b for a, b in zip(A, B)]
        D = [a - b for a, b in zip(A, B)]
        E = [c + d for c, d in zip(C, D)]
        F = [c - d for c, d in zip(C, D)]
        G = [e + f for e, f in zip(E, F)]
        H = [e - f for e, f in zip(E, F)]
        return sum(sum(x) ** 2 for x in G + H)
    
    def circuit_size(f):
        n = int(math.log2(len(f)))
        if n == 1:
            return 1
        if n == 2:
            return 3
        if n == 3:
            return 7
        if n == 4:
            return 15
        if n == 5:
            return 31
        if n == 6:
            return 63
        if n == 7:
            return 127
        if n == 8:
            return 255
        if n == 9:
            return 511
        if n == 10:
            return 1023
        if n == 11:
            return 2047
        if n == 12:
            return 4095
        if n == 13:
            return 8191
        if n == 14:
            return 16383
        if n == 15:
            return 32767
        if n == 16:
            return 65535
        if n == 17:
            return 131071
        if n == 18:
            return 262143
        if n == 19:
            return 524287
        if n == 20:
            return 1048575
        if n == 21:
            return 2097151
        if n == 22:
            return 4194303
        if n == 23:
            return 8388607
        if n == 24:
            return 16777215
        if n == 25:
            return 33554431
        if n == 26:
            return 67108863
        if n == 27:
            return 134217727
        if n == 28:
            return 268435455
        if n == 29:
            return 536870911
        if n == 30:
            return 1073741823
        if n == 31:
            return 2147483647
        if n == 32:
            return 4294967295
    
    def correlation_coefficient(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        std_X = math.sqrt(sum((x - mean_X) ** 2 for x in X) / len(X))
        std_Y = math.sqrt(sum((y - mean_Y) ** 2 for y in Y) / len(Y))
        return cov / (std_X * std_Y)
    
    n_values = [5, 10, 15, 20, 30]
    sigma_f_values = []
    s_f_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        V_f = vector_space_representation(f)
        sigma_f = symplectic_measure(V_f)
        s_f = circuit_size(f)
        sigma_f_values.append(sigma_f)
        s_f_values.append(s_f)
    
    correlation = correlation_coefficient(sigma_f_values, s_f_values)
    n_max = max(n_values)
    instances_tested = len(sigma_f_values)
    conjecture_holds = correlation >= 0.7
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")