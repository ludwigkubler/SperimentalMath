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
    n = 64
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                a = bin(i)[2:].zfill(n)
                b = bin(j)[2:].zfill(n)
                M[i][j] = f[int(a + b, 2)]
        return M
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(n-1, i-1, -1):
                M[i][j] /= M[i][i]
            for k in range(m):
                if k != i and M[k][i] != 0:
                    factor = M[k][i]
                    for j in range(i, n):
                        M[k][j] -= factor * M[i][j]
        return M
    
    def real_rank(M):
        M = gaussian_elimination(M)
        if M is None:
            return 0
        rank = sum(1 for row in M if any(row))
        return rank
    
    f = generate_boolean_function(n)
    M = communication_matrix(f)
    rank = real_rank(M)
    
    conjecture_holds = rank >= math.log2(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")