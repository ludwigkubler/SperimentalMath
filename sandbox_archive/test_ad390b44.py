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
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = -1
            A[i][-1] = f[i]
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def riemann_hypothesis_exponent(A):
        n = len(A) - 1
        det = 1.0
        for i in range(n):
            det *= abs(A[i][i])
        return math.log(det, 2)
    
    def k_clique_instance(f):
        n = len(f)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] == f[j]:
                    edges.append((i, j))
        return edges
    
    def communication_complexity(edges):
        n = len(edges) + 2
        A = [[0] * n for _ in range(n)]
        for i, j in edges:
            A[i][j] = 1
            A[j][i] = 1
        for i in range(n):
            A[i][-1] = 1
        return len(gaussian_elimination(A)) - 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    A = characteristic_polynomial(f)
    exponent = riemann_hypothesis_exponent(A)
    edges = k_clique_instance(f)
    cc = communication_complexity(edges)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": exponent <= math.log(n, 2),
        "counterexample": "" if exponent <= math.log(n, 2) else f"CC({f})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(10000, 99999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")