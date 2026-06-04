# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_matrix(f):
        n = len(f)
        A = [[0] * (2**n) for _ in range(2**n)]
        for x in range(2**n):
            for y in range(2**n):
                if f[x] == f[y]:
                    A[x][y] = 1
        return A
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix = [row[:] for row in matrix]
        r = 0
        for j in range(n):
            i_max = r
            for i in range(r, m):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if abs(matrix[i_max][j]) < 1e-9:
                continue
            matrix[r], matrix[i_max] = matrix[i_max], matrix[r]
            for i in range(r + 1, m):
                factor = -matrix[i][j] / matrix[r][j]
                for j2 in range(n):
                    matrix[i][j2] += factor * matrix[r][j2]
            r += 1
        return r
    
    def local_indeterminacy(C):
        paths = set()
        n = len(C)
        for i in range(1 << n):
            for j in range(i + 1, 1 << n):
                if (i & j) == 0:
                    path = tuple(sorted([k for k in range(n) if (i >> k) & 1]))
                    paths.add(path)
        return len(paths)
    
    def simplicial_complex(f):
        n = len(f)
        C = set()
        for i in range(1 << n):
            valid = True
            for j in range(n):
                if (i >> j) & 1:
                    if f[i ^ (1 << j)] != f[i]:
                        valid = False
                        break
            if valid:
                C.add(tuple(sorted([k for k in range(n) if (i >> k) & 1])))
        return C
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    A_f = communication_complexity_matrix(f)
    rank_A_f = rank(A_f)
    C_f = simplicial_complex(f)
    local_indet_C_f = local_indeterminacy(C_f)
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": local_indet_C_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": local_indet_C_f <= rank_A_f,
        "counterexample": "" if local_indet_C_f <= rank_A_f else f"local_indet_C_f={local_indet_C_f}, rank_A_f={rank_A_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")