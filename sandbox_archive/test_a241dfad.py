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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quasi_quadratic_form(f):
        n = int(math.log2(len(f)))
        Q_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                for x in range(2**n):
                    if f[x ^ (1 << i)] != f[x ^ (1 << j)]:
                        Q_f[i][j] += 1
                        Q_f[j][i] += 1
        return Q_f
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            rank += 1
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def ac0_parity_circuit_size(f):
        n = int(math.log2(len(f)))
        circuit_size = 0
        for i in range(n):
            if f[1 << i] != f[0]:
                circuit_size += 1
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        Q_f = compute_quasi_quadratic_form(f)
        R_Q_f = matrix_rank(Q_f)
        circuit_size = ac0_parity_circuit_size(f)
        
        if R_Q_f == 0 or circuit_size == 0:
            continue
        
        results.append({
            "n": n,
            "R_Q_f": R_Q_f,
            "circuit_size": circuit_size
        })
    
    if not results:
        return {
            "metric_name": "AC0 Parity Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_circuit_size = sum(result["circuit_size"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["circuit_size"] >= 2**(result["R_Q_f"]) / 2**(0.25 * result["n"])) / len(results)
    
    return {
        "metric_name": "AC0 Parity Circuit Size",
        "metric_value": mean_circuit_size,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"First failing seed with n={results[0]['n']}, R(Q_f)={results[0]['R_Q_f']}, circuit_size={results[0]['circuit_size']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_circuit_size = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid instances found")