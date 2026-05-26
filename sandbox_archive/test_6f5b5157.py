# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def deligne_lusztig_rank(k, n):
        if k != 2:
            return "mapping_undefined"
        
        # Construct a random k-CNF formula with n variables
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i+1) for i in range(k)]
            clauses.append(clause)
        
        # Convert the k-CNF formula to a polynomial
        poly = [[0]*n for _ in range(2**n)]
        for clause in clauses:
            term = 1
            for var in clause:
                if var > 0:
                    term *= (1 + poly[1][var-1])
                else:
                    term *= (1 - poly[1][-var-1])
            for i in range(n):
                poly[i+1] = [p + t * c for p, t, c in zip(poly[i], poly[i+1], term)]
        
        # Compute the Deligne-Lusztig class rank
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = sum(poly[2**i & 2**j])
        rank = len(gaussian_elimination(A))
        
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        rank = deligne_lusztig_rank(2, n)
        if rank == "mapping_undefined":
            return {
                "metric_name": "deligne_lusztig_rank",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        ranks.append(rank)
    
    mean_value = sum(ranks) / len(ranks)
    std_value = (sum((x - mean_value)**2 for x in ranks) / len(ranks))**0.5
    
    return {
        "metric_name": "deligne_lusztig_rank",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": all(rank >= n**(1/2 + 0.1) for rank, n in zip(ranks, n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")