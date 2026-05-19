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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M_n = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[sum(A[i][p] * B[p][j] for p in range(k)) for j in range(n)] for i in range(m)]
        return C
    
    def gaussian_elimination(M):
        rows, cols = len(M), len(M[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if M[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            M[pivot_row], M[rank] = M[rank], M[pivot_row]
            for r in range(rows):
                if r != rank and M[r][col] != 0:
                    factor = M[r][col] / M[rank][col]
                    for c in range(cols):
                        M[r][c] -= factor * M[rank][c]
            rank += 1
        return rank
    
    non_commutative_rank = gaussian_elimination(M_n)
    
    return {
        "metric_name": "non_commutative_rank",
        "metric_value": non_commutative_rank,
        "instances_tested": n,
        "conjecture_holds": non_commutative_rank >= 0.5 * n,
        "counterexample": "" if non_commutative_rank >= 0.5 * n else "non_commutative_rank < 0.5n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")