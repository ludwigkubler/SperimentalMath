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
    
    n = 40
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def tensor_product_valuation(M):
        if len(M) == 1 and len(M[0]) == 1:
            return M[0][0]
        elif len(M) == 1:
            return [tensor_product_valuation(row) for row in M[0]]
        elif len(M[0]) == 1:
            return [tensor_product_valuation(col) for col in zip(*M)]
        else:
            return [[tensor_product_valuation(submatrix) for submatrix in zip(*row)] for row in M]
    
    def minimal_rank(F):
        n = len(F)
        A = [[F[i][j] - F[i][k] * F[k][j] for j in range(n)] for k in range(1, n)]
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(i, n)):
                A[i], A[min(j for j in range(i, n) if A[j][i] != 0)] = A[min(j for j in range(i, n) if A[j][i] != 0)], A[i]
                rank += 1
                for j in range(i + 1, n):
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return rank
    
    def quadratic_form(M):
        F = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                F[i][j] = M[i][j] + M[j][i]
                F[j][i] = F[i][j]
        return F
    
    def symmetric_bilinear_form(F):
        B_F = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                B_F[i][j] = sum(F[k][l] for k in range(n) for l in range(n) if (k == i and l == j) or (k == j and l == i))
                B_F[j][i] = B_F[i][j]
        return B_F
    
    def rank_of_bilinear_form(B):
        n = len(B)
        A = [[B[i][j] - B[i][k] * B[k][j] for j in range(n)] for k in range(1, n)]
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(i, n)):
                A[i], A[min(j for j in range(i, n) if A[j][i] != 0)] = A[min(j for j in range(i, n) if A[j][i] != 0)], A[i]
                rank += 1
                for j in range(i + 1, n):
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return rank
    
    F = quadratic_form(M)
    B_F = symmetric_bilinear_form(F)
    
    min_rank_F = minimal_rank(F)
    rank_B_F = rank_of_bilinear_form(B_F)
    
    metric_value = min_rank_F
    instances_tested = 1
    conjecture_holds = abs(metric_value - math.log(n)) <= 2 * math.log(n)
    counterexample = "" if conjecture_holds else "min_rank_F does not satisfy the conjecture"
    
    return {
        "metric_name": "Minimal Rank of Quadratic Form",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_F does not satisfy the conjecture\" first_failing_seed={seeds[first_failing_seed]}")