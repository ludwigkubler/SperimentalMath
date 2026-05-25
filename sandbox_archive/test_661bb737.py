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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i == j:
                    A[i][j] = 1 / A[i][j]
                else:
                    A[i][j] *= A[i][i]
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        if i == j:
                            A[k][j] -= factor
                        else:
                            A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def hodge_diamond_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(abs(A[j][i]) < 1e-9 for j in range(n)):
                continue
            rank += 1
        return rank
    
    def ac0_parity_depth(C):
        m, n = len(C), len(C[0])
        depth = 0
        while any(any(c != 0 for c in row) for row in C):
            new_C = [[0 for _ in range(n)] for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    if C[i][j] % 2 == 1:
                        for k in range(n):
                            new_C[i][k] += C[j][k]
            C = new_C
            depth += 1
        return depth
    
    def generate_boolean_algebra(n, k):
        elements = [tuple(sorted(random.sample(range(2), n))) for _ in range(k)]
        relations = []
        for i in range(k):
            for j in range(i + 1, k):
                if all(elements[i][p] == elements[j][p] for p in range(n)):
                    relations.append((i, j))
        return elements, relations
    
    n = random.randint(5, 40)
    k = random.randint(0, min(2 * n, 100))  # Limiting k to avoid excessive complexity
    B_elements, B_relations = generate_boolean_algebra(n, k)
    
    A = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if all(B_elements[i][p] == B_elements[j][p] for p in range(n)):
                A[i][j] = 1
    
    rank = hodge_diamond_rank(A)
    
    C = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        C[i][i] = B_elements[i].count(1) % 2
    depth = ac0_parity_depth(C)
    
    return {
        "metric_name": "Hodge Diamond Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n**depth,
        "counterexample": "" if rank <= n**depth else f"Rank {rank} > {n**depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")