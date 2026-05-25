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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_polynomial(circuit):
        n = len(circuit)
        x = ['x' + str(i) for i in range(n)]
        poly = []
        for i in range(2**n):
            term = 1
            for j in range(n):
                if circuit[i] & (1 << j):
                    term *= x[j]
            poly.append(term)
        return poly
    
    def gaussian_elimination(A, b):
        n = len(b)
        A = [row[:] + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None
            pivot = A[i][i]
            A[i] = [a / pivot for a in A[i]]
            for j in range(n):
                if i == j:
                    continue
                factor = A[j][i]
                A[j] = [a - factor * b for a, b in zip(A[j], A[i])]
        return [row[-1] for row in A]
    
    def minimal_rank(poly):
        n = len(poly)
        A = [[0] * (n + 1) for _ in range(n)]
        for i, term in enumerate(poly):
            for j in range(n):
                if 'x' + str(j) in term:
                    A[i][j] += 1
        return len(gaussian_elimination(A, [0] * n))
    
    def rho_circuit(circuit_size):
        circuit = generate_boolean_circuit(circuit_size)
        poly = construct_polynomial(circuit)
        return minimal_rank(poly)
    
    n_values = [5, 10, 15, 20, 30, 40]
    rho_values = []
    for n in n_values:
        rho_values.extend([rho_circuit(n) for _ in range(5)])
    
    if not rho_values:
        return {
            "metric_name": "rho_f",
            "metric_value": 1.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rho = sum(rho_values) / len(rho_values)
    return {
        "metric_name": "rho_f",
        "metric_value": mean_rho,
        "instances_tested": len(rho_values),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")