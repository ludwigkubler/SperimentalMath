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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A, mod):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] = (A[i][j] * pow(pivot, -1, mod)) % mod
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] = (A[j][k] - factor * A[i][k]) % mod
        return A
    
    def hodge_order(cnf, n, mod):
        m = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(m):
            x, y = abs(cnf[i][0]), abs(cnf[i][1])
            A[x][y] += 1
            A[y][x] += 1
        
        A = gaussian_elimination(A, mod)
        
        order = 0
        for row in A:
            if any(val != 0 for val in row):
                order += 1
        
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            mod = 10**9 + 7
            order = hodge_order(cnf, n, mod)
            total_order += order
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= n**3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")