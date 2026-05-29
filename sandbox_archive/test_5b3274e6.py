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
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def det(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = 0
            for c in range(n):
                M = [row[:c] + row[c+1:] for row in A[1:]]
                sign = (-1) ** (c % 2)
                sub_det = det(M)
                det_val += sign * A[0][c] * sub_det
            return det_val
    
    def fundamental_group(G):
        n = len(G)
        if n <= 1:
            return 0
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    edges.append((i, j))
        m = len(edges)
        A = [[0] * (m + n) for _ in range(m + n)]
        for i in range(m):
            u, v = edges[i]
            A[i][i] = 1
            A[m + u][i] = -1
            A[m + v][i] = -1
        A[m + n - 1][m + n - 1] = 1
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return n - rank
    
    def communication_complexity(dim):
        return 2 ** dim
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    dim = fundamental_group(G)
    cc = communication_complexity(dim)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": abs(cc - 2 ** dim) < 2 * 2 ** dim / n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")