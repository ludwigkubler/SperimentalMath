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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find pivot
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        return A
    
    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                submatrix = [row[:c] + row[c+1:] for row in A[1:]]
                det += ((-1) ** c) * A[0][c] * determinant(submatrix)
        
        return det
    
    def is_full_rank(A):
        return abs(determinant(A)) > 1e-9
    
    def generate_polynomial(n, degree):
        coefficients = [random.randint(0, 100) for _ in range(degree + 1)]
        return coefficients
    
    def construct_incidence_graph(f, n):
        graph = set()
        for x in range(n):
            y = sum(c * (x ** i) for i, c in enumerate(f))
            for j in range(x + 1, n):
                if sum(c * (j ** i) for i, c in enumerate(f)) == y:
                    graph.add((x, j))
        return graph
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std_dev(lst, m):
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n = random.randint(5, 40)
    D = random.randint(1, 10)
    f = generate_polynomial(n, D)
    graph = construct_incidence_graph(f, n)
    num_edges = len(graph)
    
    metric_value = num_edges / math.sqrt(n * D)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if metric_value <= 10:
        conjecture_holds = True
    
    return {
        "metric_name": "num_edges_per_sqrt_nD",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_value = mean([r["metric_value"] for r in results])
    std_dev_value = std_dev([r["metric_value"] for r in results], mean_value)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"metric_value_exceeds_10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")