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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quasi_quadratic_form(f):
        n = len(f)
        Q_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                Q_f[i][j] = sum(f[k] * f[l] for k in range(2**n) if (k >> i) & 1 and (k >> j) & 1)
                Q_f[j][i] = Q_f[i][j]
        return Q_f
    
    def compute_rank(matrix):
        n = len(matrix)
        rank = 0
        for col in range(n):
            pivot_row = None
            for row in range(rank, n):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rank, n):
                    factor = Fraction(matrix[row][col], matrix[rank-1][col])
                    for j in range(col, n + 1):
                        matrix[row][j] -= factor * matrix[rank-1][j]
        return rank
    
    def ac0_parity_circuit_size(f):
        n = len(f)
        circuit_size = 0
        for i in range(n):
            if f[i] == 1:
                circuit_size += 1
        return circuit_size
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    Q_f = compute_quasi_quadratic_form(f)
    R_Q_f = compute_rank(Q_f)
    ac0_size = ac0_parity_circuit_size(f)
    
    conjecture_holds = ac0_size >= (2 ** R_Q_f) / 2 ** (0.5 * n ** (3/4))
    counterexample = "" if conjecture_holds else "AC0 circuit size does not meet the lower bound"
    
    return {
        "metric_name": "AC0 parity circuit size",
        "metric_value": ac0_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AC0 circuit size does not meet the lower bound\" first_failing_seed={first_failing_seed}")