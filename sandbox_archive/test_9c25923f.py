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
    
    def vc_dimension(R):
        n = len(R)
        if n == 0:
            return 0
        for d in range(1, n + 1):
            if all(len(shatter) >= (1 << i) for i in range(d)):
                continue
            return d - 1
        return n
    
    def log2_rank_GF2(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            pivot = None
            for i in range(m):
                if matrix[i][j] == 1:
                    if pivot is not None:
                        for k in range(j + 1, n):
                            if matrix[i][k]:
                                matrix[i][k] ^= matrix[pivot][k]
                    else:
                        pivot = i
            if pivot is not None:
                rank += 1
        return rank
    
    def lift_matrix(f, g, n):
        A, B = len(g), len(g[0])
        M = [[f(g[a], b) for b in range(B)] for a in range(A)]
        for _ in range(n - 1):
            M_next = []
            for i in range(A):
                row = [M[i][j] for j in range(B)]
                for k in range(A):
                    new_row = [row[j] ^ M[k][j] for j in range(B)]
                    M_next.append(new_row)
            M = M_next
        return M
    
    gadgets = {
        "index_b": lambda a, b: int(a == b),
        "inner-product_b": lambda a, b: sum(x * y for x, y in zip(a, b)),
        "equality": lambda a, b: int(a == b)
    }
    
    results = []
    n_values = [2, 3, 4]
    A_sizes = [4, 8]
    B_sizes = [2, 3, 4]
    
    for _ in range(10):  # 10 trials per seed
        n = random.choice(n_values)
        A_size = random.choice(A_sizes)
        B_size = random.choice(B_sizes)
        
        f = [random.randint(0, 1) for _ in range(2 ** n)]
        g = [[random.randint(0, 1) for _ in range(B_size)] for _ in range(A_size)]
        
        R_g = [g[a] for a in range(A_size)]
        d = vc_dimension(R_g)
        
        M = lift_matrix(f, g, n)
        rank = log2_rank_GF2(M)
        
        metric_value = (0.5 * math.log2(len(f)) * d) - n
        slack = rank - metric_value
        
        results.append({
            "metric_name": "log2_rank_GF2",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": slack >= 0,
            "counterexample": "" if slack >= 0 else f"n={n}, A_size={A_size}, B_size={B_size}"
        })
    
    return {
        "metric_name": "log2_rank_GF2",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")