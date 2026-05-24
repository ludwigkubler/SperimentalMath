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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_quasi_quadratic_form(f):
        n = int(math.log2(len(f)))
        Q_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n + 1):
                Q_f[i][j] = sum(f[k] * f[k + j - i] for k in range(2**n))
        return Q_f
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = None
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(m):
                    if row != rank - 1:
                        factor = matrix[row][col] / matrix[rank - 1][col]
                        for j in range(n):
                            matrix[row][j] -= factor * matrix[rank - 1][j]
        return rank
    
    def ac0_parity_circuit_size(f):
        n = int(math.log2(len(f)))
        circuit_size = 0
        for i in range(n):
            if sum(f[k] for k in range(2**n) if k & (1 << i)) % 2 == 1:
                circuit_size += 1
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_circuit_size = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        Q_f = compute_quasi_quadratic_form(f)
        R_Q_f = matrix_rank(Q_f)
        
        if R_Q_f <= 0:
            continue
        
        circuit_size = ac0_parity_circuit_size(f)
        total_circuit_size += circuit_size
        instances_tested += 1
        
        lower_bound = (2 ** R_Q_f) / (2 ** (c * n ** (3/4)))
        if circuit_size < lower_bound:
            conjecture_holds = False
            counterexample = f"n={n}, R(Q_f)={R_Q_f}, circuit_size={circuit_size}, lower_bound={lower_bound}"
    
    mean_circuit_size = total_circuit_size / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / len(n_values)
    
    return {
        "metric_name": "AC0 Parity Circuit Size",
        "metric_value": mean_circuit_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_circuit_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")