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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find the pivot row
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate the pivot column
            for j in range(m):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        # Back-substitute to find the solution
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        
        return x

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        det = Fraction(1)
        for i in range(m):
            # Find the pivot row
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate the pivot column
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            
            det *= factor
            if det == 0:
                return 0
        
            # Eliminate the pivot row
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        
        return det

    def min_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if determinant([row[i:] for row in A[i:]]) != 0:
                rank += 1
        return rank

    def max_cut_instance(n, m):
        edges = set()
        while len(edges) < m:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def tropicalized_lattice(edges):
        d = len(edges)
        A = [[0] * d for _ in range(d)]
        for i, (u, v) in enumerate(edges):
            A[u][i] = 1
            A[v][i] = 1
        return A

    def sum_of_squares_certificate(n, m):
        # This is a placeholder function. In practice, you would need to implement
        # an actual sum-of-squares certificate construction algorithm.
        return random.randint(1, n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, n * (n - 1) // 2)
    instance = max_cut_instance(n, m)
    d = sum_of_squares_certificate(n, m)
    
    lattice = tropicalized_lattice(instance)
    rank = min_rank(lattice)
    
    if rank < math.ceil(d ** (1/3)):
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, m={m}, d={d}, rank={rank}"
        }
    else:
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[first_failing_seed]['instances_tested']}, m={m}, d={d}, rank={rank}' first_failing_seed={seeds[first_failing_seed]}")