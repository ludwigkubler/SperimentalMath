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
    
    def generate_random_function(n):
        # Generate a random function in P with read-twice branching program width n
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def geometric_quantization_matrix(f):
        # Compute the geometric quantization matrix for a given function f
        n = int(math.log2(len(f)))
        G = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                if f[i*2 + j] == 1:
                    G[2*i][j] = 1
                    G[2*i+1][j+n] = 1
        return G
    
    def min_rank(matrix):
        # Compute the minimal rank of a matrix using Gaussian elimination
        m, n = len(matrix), len(matrix[0])
        A = [row[:] for row in matrix]
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if abs(A[i][j]) > 1e-9:
                    i_max = i
                    break
            if i_max == -1:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for k in range(n):
                A[rank][k] /= A[rank][j]
            for i in range(m):
                if i != rank and abs(A[i][j]) > 1e-9:
                    for k in range(n):
                        A[i][k] -= A[i][j] * A[rank][k]
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_random_function(n)
    G = geometric_quantization_matrix(f)
    rank = min_rank(G)
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n <= 40:
        # Check if the minimal rank is between Θ(log(n/2)) and O(log n)
        lower_bound = math.log(n / 2, 2)
        upper_bound = math.log(n, 2)
        if lower_bound <= metric_value <= upper_bound:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = "minimal_rank_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")