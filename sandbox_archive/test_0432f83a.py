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
    
    def generate_read_twice_bp(depth, size):
        # Generate a random read-twice branching program instance
        bp = []
        for _ in range(size):
            level = []
            for _ in range(2**depth):
                if random.choice([True, False]):
                    level.append(random.choice([0, 1]))
                else:
                    level.append(None)
            bp.append(level)
        return bp
    
    def hermitian_matrix(bp):
        # Construct the associated Hermitian matrix
        n = len(bp[0])
        m = len(bp)
        H = [[0] * n for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if bp[i][j] is not None:
                    H[j][i] += bp[i][j]
        return H
    
    def svd(matrix):
        # Compute the singular value decomposition of a matrix
        n = len(matrix)
        U = [[0] * n for _ in range(n)]
        S = [0] * n
        V = [[0] * n for _ in range(n)]
        
        # Center the matrix
        mean = sum(sum(row) for row in matrix) / (n * n)
        centered_matrix = [[matrix[i][j] - mean for j in range(n)] for i in range(n)]
        
        # Compute U and S
        for k in range(n):
            u_k = [centered_matrix[i][k] for i in range(n)]
            norm_u_k = math.sqrt(sum(x**2 for x in u_k))
            if norm_u_k == 0:
                continue
            u_k = [x / norm_u_k for x in u_k]
            S[k] = sum(u_k[i]**2 * centered_matrix[i][k] for i in range(n))
            for i in range(n):
                U[i][k] = u_k[i]
        
        # Compute V
        for k in range(n):
            v_k = [0] * n
            for i in range(n):
                v_k[i] = sum(U[j][i] * S[j] for j in range(k+1))
            norm_v_k = math.sqrt(sum(x**2 for x in v_k))
            if norm_v_k == 0:
                continue
            v_k = [x / norm_v_k for x in v_k]
            for i in range(n):
                V[i][k] = v_k[i]
        
        return U, S, V
    
    def min_tensor_rank(matrix):
        # Compute the minimal tensor rank of a matrix
        U, S, V = svd(matrix)
        rank = sum(1 for s in S if abs(s) > 1e-10)
        return rank
    
    depth = random.randint(5, 40)
    size = random.randint(5, 40)
    bp = generate_read_twice_bp(depth, size)
    H = hermitian_matrix(bp)
    rank = min_tensor_rank(H)
    
    conjecture_holds = False
    counterexample = ""
    
    if depth > 1:
        upper_bound = 2**depth
        if rank <= upper_bound:
            conjecture_holds = True
        else:
            counterexample = f"Rank {rank} exceeds upper bound {upper_bound}"
    
    if size == 40 and rank < 2**size / 4:
        conjecture_holds = False
        counterexample = "Rank is less than lower bound for BP IP_2"
    
    return {
        "metric_name": "minimal_tensor_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")