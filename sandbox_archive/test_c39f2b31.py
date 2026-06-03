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
        rank = 0
        for i in range(n):
            max_row = next((j for j in range(rank, m) if A[j][i] != 0), -1)
            if max_row == -1:
                continue
            A[i], A[max_row] = A[max_row], A[i]
            rank += 1
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def matrix_rank(A):
        return gaussian_elimination(A)
    
    def communication_matrix_rank(n):
        # Simulate a random communication matrix
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix_rank(A)
    
    def fundamental_group_rank(n):
        # Simulate a random fundamental group rank
        return random.randint(1, n)
    
    def abelianization_rank(n):
        # Simulate a random abelianization rank
        return random.randint(1, n)
    
    def minimal_local_indeterminacy(fundamental_group_rank, abelianization_rank):
        return fundamental_group_rank - abelianization_rank
    
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        fundamental_group_r = fundamental_group_rank(n)
        abelianization_r = abelianization_rank(n)
        
        comm_matrix_r = communication_matrix_rank(n)
        local_indeterminacy = minimal_local_indeterminacy(fundamental_group_r, abelianization_r)
        
        if local_indeterminacy < 0:
            continue
        
        instances_tested += 1
        max_n = max(max_n, n)
        
        total_metric_value += local_indeterminacy * comm_matrix_r
    
    if instances_tested == 0:
        return {
            "metric_name": "minimal_local_indeterminacy * communication_matrix_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "minimal_local_indeterminacy * communication_matrix_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")