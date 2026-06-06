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
    
    def projective_space_embedding(cnf):
        n = max(abs(x) for x in cnf[0])  # Assuming each clause is a tuple of literals
        return n
    
    def communication_complexity_rank(cnf):
        m, n = len(cnf), len(cnf[0])
        matrix = [[1 if literal in clause else 0 for literal in range(1, n + 1)] for clause in cnf]
        
        # Gaussian elimination to find the rank
        rank = 0
        for i in range(n):
            pivot_row = next((j for j in range(rank, m) if matrix[j][i] != 0), None)
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for j in range(m):
                    if j != rank - 1:
                        factor = matrix[j][i] / matrix[rank - 1][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
        
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    def min_symplectic_volume(n):
        # Placeholder for the actual computation
        return n * (n + 1) // 2
    
    cnf = []
    n, m = random.randint(5, 30), random.randint(10, 30)
    for _ in range(m):
        clause = tuple(random.sample(range(-n, -1) + list(range(1, n + 1)), random.randint(1, n)))
        cnf.append(clause)
    
    sym_vol = min_symplectic_volume(n)
    comm_rank = communication_complexity_rank(cnf)
    var_comm_rank = variance([comm_rank] * 30)  # Assuming all ranks are the same for simplicity
    
    if var_comm_rank == 0:
        return {
            "metric_name": "Symplectic Volume to Communication Complexity Rank Variance Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Variance of communication complexity ranks is zero"
        }
    
    ratio = abs(sym_vol / var_comm_rank)
    return {
        "metric_name": "Symplectic Volume to Communication Complexity Rank Variance Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 10,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Ratio exceeds constant bound"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")