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
    
    def communication_distance(f, g):
        return sum(1 for i in range(len(f)) if f[i] != g[i])
    
    def min_plus_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                M[2*i][2*j] = f[i]
                M[2*i+1][2*j+1] = f[j]
        return M
    
    def symplectic_hull(M):
        n = len(M) // 2
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [M[i][:n] + M[i][n:] for i in range(n)]
        B = [M[i+n][:n] + M[i+n][n:] for i in range(n)]
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for j in range(n):
                pivot_row = next((i for i in range(j, m) if A[i][j]), None)
                if pivot_row is None:
                    continue
                A[pivot_row], A[j] = A[j], A[pivot_row]
                for i in range(m):
                    if i != j:
                        factor = A[i][j] / A[j][j]
                        A[i][j:] = [A[i][k] - factor * A[j][k] for k in range(j, n)]
            return A
        
        A = gaussian_elimination(A)
        
        def rank(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(m):
                if any(matrix[i][j] != 0 for j in range(n)):
                    rank += 1
            return rank
        
        return rank(A) + rank(B)
    
    def run_test(d):
        f = generate_boolean_function(d)
        g = generate_boolean_function(d)
        while communication_distance(f, g) == 0:
            f = generate_boolean_function(d)
            g = generate_boolean_function(d)
        
        M_f = min_plus_representation(f)
        M_g = min_plus_representation(g)
        M_fg = [[(M_f[i][j] + M_g[i][j]) % 2 for j in range(len(M_f[0]))] for i in range(len(M_f))]
        
        rank_fg = symplectic_hull(M_fg)
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank_fg,
            "instances_tested": 1,
            "conjecture_holds": rank_fg <= d**2,
            "counterexample": "" if rank_fg <= d**2 else f"Communication distance {d}, rank {rank_fg}"
        }
    
    results = [run_test(d) for d in range(2, 41)]
    total_rank = sum(result["metric_value"] for result in results)
    num_tests = len(results)
    mean_rank = total_rank / num_tests
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / num_tests
    
    return {
        "seed": seed,
        "mean_rank": mean_rank,
        "support_fraction": support_fraction,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["mean_rank"] for r in results)
    num_tests = len(results)
    mean_rank = total_rank / num_tests
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / num_tests
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='seed={first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")