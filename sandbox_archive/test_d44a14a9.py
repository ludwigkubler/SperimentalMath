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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def svd(A):
        m, n = len(A), len(A[0])
        U = [[random.random() for _ in range(m)] for _ in range(m)]
        V = [[random.random() for _ in range(n)] for _ in range(n)]
        S = [1.0] * min(m, n)
        
        for _ in range(100):  # Simple power iteration for SVD
            U = gaussian_elimination(U)
            V = gaussian_elimination(V)
            A = [[sum(A[i][k] * V[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
            U = [[sum(A[i][k] * U[j][k] for k in range(m)) for j in range(m)] for i in range(m)]
        
        return U, S, V

    def hermitian_matrix(n):
        M = [[random.random() + 1j * random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                M[j][i] = M[i][j].conjugate()
        return M

    def tensor_rank(M):
        U, S, V = svd(M)
        rank = sum(1 for s in S if abs(s) > 1e-6)
        return rank
    
    n = random.randint(5, 40)
    d = random.randint(5, 40)
    
    M = hermitian_matrix(n)
    rank = tensor_rank(M)
    
    conjecture_holds = rank <= 2**d and (rank >= 2**n / 4 if n == 2 else True)
    counterexample = "" if conjecture_holds else f"Rank {rank} > 2^{d}"
    
    return {
        "metric_name": "Tensor Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")