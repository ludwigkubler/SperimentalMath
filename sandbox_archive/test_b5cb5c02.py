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
    
    def generate_channel(n):
        return [[random.random() for _ in range(n)] for _ in range(n)]
    
    def choi_isomorphism(channel):
        n = len(channel)
        choi_matrix = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        choi_matrix[i*n + j][k*n + l] += channel[i][j] * channel[k][l]
        return choi_matrix
    
    def qr_decomposition(matrix):
        m, n = len(matrix), len(matrix[0])
        Q = [[0] * n for _ in range(n)]
        R = [[0] * n for _ in range(n)]
        
        for k in range(n):
            norm_v = 0
            for i in range(k, m):
                norm_v += matrix[i][k]**2
            norm_v = math.sqrt(norm_v)
            
            if norm_v == 0:
                continue
            
            Q[k][k] = v[k] / norm_v
            R[k][k] = norm_v
            
            for j in range(k+1, n):
                R[k][j] = sum(matrix[i][k] * matrix[i][j] for i in range(k, m))
                for i in range(k, m):
                    Q[i][j] = (matrix[i][k] * matrix[i][j]) / norm_v
        
        return Q, R
    
    def eigenvalues(matrix):
        n = len(matrix)
        eigs = []
        
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v_norm = sum(x**2 for x in v)**0.5
            v = [x / v_norm for x in v]
            
            w = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            w_norm = sum(x**2 for x in w)**0.5
            
            eigs.append(sum(w[i] * v[i] for i in range(n)))
        
        return eigs
    
    def non_commutative_entropy(eigs):
        entropy = 0
        for eig in eigs:
            if eig > 0:
                entropy -= eig * math.log2(eig)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        channel = generate_channel(n)
        choi = choi_isomorphism(channel)
        eigs = eigenvalues(choi)
        entropy = non_commutative_entropy(eigs)
        
        total_entropy += entropy
        instances_tested += len(eigs)
        n_max = max(n_max, n)
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = all(abs(mean_entropy - C) <= 10 * C for C in [n**2 for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "non_commutative_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")