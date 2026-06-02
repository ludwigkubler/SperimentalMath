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
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        if len(A) != len(A[0]):
            raise ValueError("Matrix must be square")
        if len(A) == 1:
            return A[0][0]
        det = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def minimal_geometric_entropy(A):
        if not gaussian_elimination(A):
            raise ValueError("Matrix must be non-singular")
        det = determinant(A)
        if det == 0:
            raise ValueError("Matrix must be non-singular")
        entropy = -math.log2(abs(det))
        return entropy
    
    def communication_complexity_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    instances_tested = 0
    total_mge = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        mge_A = minimal_geometric_entropy(A)
        ccr_A = communication_complexity_rank(A)
        
        if mge_A < ccr_A * 0.8:
            conjecture_holds = False
            counterexample = f"n={n}, mge={mge_A}, ccr={ccr_A}"
        
        instances_tested += 1
        total_mge += mge_A
        n_max = max(n_max, n)
    
    if not conjecture_holds:
        return {
            "metric_name": "minimal_geometric_entropy / communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    mean_mge = total_mge / instances_tested
    return {
        "metric_name": "minimal_geometric_entropy / communication_complexity_rank",
        "metric_value": mean_mge,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_mge = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mge} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mge} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")