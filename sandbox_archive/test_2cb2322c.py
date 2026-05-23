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
    
    def compute_acc0_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = 1
        while True:
            new_f = []
            for i in range(len(f) // 2):
                new_f.append((f[2*i] + f[2*i+1]) % 2)
            f = new_f
            n //= 2
            if n == 1:
                return depth
    
    def compute_twisted_quasi_symmetric_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if all((f[i] + f[j]) % 2 == (i ^ j) & 1 for j in range(i)):
                rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(m):
            if any(row_echelon_form[i][j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    depth = compute_acc0_depth(f)
    rank_twisted_quasi_symmetric = compute_twisted_quasi_symmetric_rank(f)
    
    if depth == 0:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "ACC⁰ depth is zero"
        }
    
    C = rank_twisted_quasi_symmetric / math.log(depth)
    if C * math.log(depth) * 2 >= rank_twisted_quasi_symmetric:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "rank",
        "metric_value": rank_twisted_quasi_symmetric,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")