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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def entanglement_complexity(circuit):
        # Placeholder function. Replace with actual computation.
        return len(circuit)

    def construct_twisted_module(circuit):
        n = len(circuit)
        module_order = 2 ** n
        return module_order

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit_size = random.randint(1, n)
        circuit = [random.choice([0, 1]) for _ in range(circuit_size)]
        e_C = entanglement_complexity(circuit)
        M_order = construct_twisted_module(circuit)
        
        results.append({
            "n": n,
            "circuit_size": circuit_size,
            "e_C": e_C,
            "M_order": M_order
        })
    
    mean_M_order = sum(result["M_order"] for result in results) / len(results)
    fraction_supporting = sum(1 for result in results if 1 <= result["M_order"] <= result["e_C"]) / len(results)
    
    return {
        "metric_name": "Twisted Module Order",
        "metric_value": mean_M_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": fraction_supporting >= 0.8,
        "counterexample": "" if fraction_supporting >= 0.8 else f"e(C)={results[0]['e_C']}, M_order={results[0]['M_order']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    fraction_supporting = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if fraction_supporting >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={fraction_supporting}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")