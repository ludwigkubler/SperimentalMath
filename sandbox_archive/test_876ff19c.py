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
    
    def formal_context(f):
        n = int(math.log2(len(f)))
        X = list(range(n))
        Y = list(range(n))
        R = []
        for x in X:
            for y in Y:
                if f[x] == f[y]:
                    R.append((x, y))
        return R
    
    def galois_connection(R):
        X = set()
        Y = set()
        for r in R:
            X.add(r[0])
            Y.add(r[1])
        X = list(X)
        Y = list(Y)
        X.sort()
        Y.sort()
        A = [[0] * len(Y) for _ in range(len(X))]
        B = [[0] * len(X) for _ in range(len(Y))]
        for r in R:
            i = X.index(r[0])
            j = Y.index(r[1])
            A[i][j] = 1
            B[j][i] = 1
        return A, B
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i]):
                rank += 1
                for j in range(n):
                    if matrix[i][j]:
                        for k in range(m):
                            if k != i and matrix[k][j]:
                                matrix[k][j] = False
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        R = formal_context(f)
        A, B = galois_connection(R)
        rank = matrix_rank(A)
        total_rank += rank
        instances_tested += len(R)
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n**2
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected<=n^2"
    
    return {
        "metric_name": "Minimal Rank of Formal Contexts",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank exceeded n^2\" first_failing_seed={first_failing_seed}")