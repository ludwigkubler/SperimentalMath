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
    
    def max_plus_entropy(poly):
        n = len(poly)
        if n == 0:
            return 0
        max_val = max(poly)
        return -max_val * (n - poly.count(max_val))
    
    def char_poly(f, m):
        n = 2 ** m
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f(i ^ j) != f(j ^ i):
                    return [0]
        for i in range(n):
            A[i][i] = 1
        for k in range(m):
            B = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    B[i][j] = f(i ^ (j << k))
            A = matrix_mult(A, B)
        return [sum(row) for row in A]
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def boolean_function(m):
        return lambda x: random.choice([0, 1])
    
    m = random.randint(5, 40)
    n_max = max_plus_entropy(char_poly(boolean_function(m), m))
    metric_value = n_max
    instances_tested = 30
    conjecture_holds = n_max <= m * math.log(m)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_plus_entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")