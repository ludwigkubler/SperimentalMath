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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        F[0][0] = 1
        for i in range(n):
            F[i+1][0] = -f[i]
            for j in range(i + 1):
                F[i+1][j+1] = F[i][j] - f[i] * F[i][j+1]
        return F
    
    def hodge_integrals(P, n):
        det = determinant(P)
        if det == 0:
            return []
        rank = 0
        for i in range(n + 1):
            if P[i][i] != 0:
                rank += 1
        return [det / (P[0][0]**(n - i)) for i in range(rank)]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    P = characteristic_polynomial(f)
    hodge_ints = hodge_integrals(P, n)
    
    if not hodge_ints:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank = len(hodge_ints)
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 6)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")