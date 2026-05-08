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
    
    def generate_bp(n: int, read_twice: bool):
        bp = []
        for i in range(n):
            if read_twice:
                bp.append(random.choice([0, 1]))
                bp.append(random.choice([0, 1]))
            else:
                bp.append(random.choice([0, 1]))
        return bp
    
    def adjacency_matrix(bp: list) -> list:
        n = len(bp)
        adj = [[0] * n for _ in range(n)]
        for i in range(n):
            if bp[i] == 1:
                j = (i + 1) % n
                adj[i][j] = 1
                adj[j][i] = 1
        return adj
    
    def matrix_multiply(A: list, B: list) -> list:
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A: list) -> list:
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A: list) -> float:
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for i in range(n):
                submatrix = [row[:i] + row[i+1:] for row in A[1:]]
                det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det
    
    def r_transform(A: list) -> float:
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        Z = matrix_multiply(I, A)
        for k in range(2, n+1):
            Z_k = matrix_multiply(Z, A)
            det_Z_k = determinant(Z_k)
            det_A_k = determinant(A ** k)
            if det_Z_k == 0 or det_A_k == 0:
                break
            Z = [[Z[i][j] / (k * det_A_k) for j in range(n)] for i in range(n)]
        return sum(sum(Z[i][j] for j in range(i+1, n)) for i in range(n))
    
    def free_cumulant(A: list) -> float:
        R = r_transform(A)
        return 2 * R
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp_read_once = generate_bp(n, False)
        bp_read_twice = generate_bp(n, True)
        
        adj_read_once = adjacency_matrix(bp_read_once)
        adj_read_twice = adjacency_matrix(bp_read_twice)
        
        kappa_4_read_once = free_cumulant(adj_read_once)
        kappa_4_read_twice = free_cumulant(adj_read_twice)
        
        results.append({
            "n": n,
            "kappa_4_read_once": kappa_4_read_once,
            "kappa_4_read_twice": kappa_4_read_twice
        })
    
    mean_kappa_4_read_once = sum(result["kappa_4_read_once"] for result in results) / len(results)
    mean_kappa_4_read_twice = sum(result["kappa_4_read_twice"] for result in results) / len(results)
    
    conjecture_holds_read_once = all(kappa_4 >= n / 10 for kappa_4, n in zip([result["kappa_4_read_once"] for result in results], [result["n"] for result in results]))
    conjecture_holds_read_twice = all(kappa_4 <= math.log(n) + 1 for kappa_4, n in zip([result["kappa_4_read_twice"] for result in results], [result["n"] for result in results]))
    
    counterexample = ""
    if not conjecture_holds_read_once:
        counterexample += "Read-once BP: "
        for result in results:
            if result["kappa_4_read_once"] < result["n"] / 10:
                counterexample += f"n={result['n']}, kappa_4={result['kappa_4_read_once']}; "
    if not conjecture_holds_read_twice:
        counterexample += "Read-twice BP: "
        for result in results:
            if result["kappa_4_read_twice"] > math.log(result["n"]) + 1:
                counterexample += f"n={result['n']}, kappa_4={result['kappa_4_read_twice']}; "
    
    return {
        "metric_name": "Free Cumulant κ₄",
        "metric_value": (mean_kappa_4_read_once, mean_kappa_4_read_twice),
        "instances_tested": len(results) * 2,
        "conjecture_holds": conjecture_holds_read_once and conjecture_holds_read_twice,
        "counterexample": counterexample.strip()
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_kappa_4_read_once = sum(result["metric_value"][0] for result in results) / len(results)
    mean_kappa_4_read_twice = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_kappa_4_read_once} std={math.sqrt(sum((result['metric_value'][0] - mean_kappa_4_read_once) ** 2 for result in results) / len(results))} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")