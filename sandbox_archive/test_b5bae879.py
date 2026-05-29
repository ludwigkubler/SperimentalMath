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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find max element in column i
        max_idx = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_idx] = A[max_idx], A[i]
        
        # Make the pivot 1
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        
        # Eliminate other elements in column i
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def spectral_norm(A, p=2):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    v = [random.random() for _ in range(n)]
    v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    
    for _ in range(100):
        Av = matrix_multiply(A, v)
        v = Av
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    
    return sum(abs(v[i]) ** p for i in range(n)) ** (1/p)

def communication_complexity_disjointness(n):
    def send_bit(bit, sender_id):
        if bit == 0:
            return 1
        else:
            return n
    
    def receive_bits(bits, receiver_id):
        return sum(1 for bit in bits if bit == 1)
    
    bits = [random.randint(0, 1) for _ in range(n)]
    sender_id = random.randint(0, 1)
    receiver_id = 1 - sender_id
    
    if sender_id == 0:
        return send_bit(bits[0], sender_id)
    else:
        return receive_bits(bits, receiver_id)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_spectral_norm = 0
    total_comm_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            M1 = [[random.gauss(0, 1) for _ in range(n)] for _ in range(n)]
            M2 = [[random.gauss(0, 1) for _ in range(n)] for _ in range(n)]
            
            T = matrix_multiply(M1, M2)
            spectral_norm_T = spectral_norm(T)
            comm_complexity = communication_complexity_disjointness(n)
            
            total_spectral_norm += spectral_norm_T
            total_comm_complexity += comm_complexity
            instances_tested += 1
    
    avg_spectral_norm = total_spectral_norm / instances_tested
    avg_comm_complexity = total_comm_complexity / instances_tested
    
    C_n = avg_comm_complexity ** (1/2)
    
    if avg_spectral_norm >= C_n * avg_comm_complexity:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Spectral norm is less than C(n) times communication complexity"
    
    return {
        "metric_name": "spectral_norm_over_comm_complexity",
        "metric_value": avg_spectral_norm / (C_n * avg_comm_complexity),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Spectral norm is less than C(n) times communication complexity\" first_failing_seed={first_failing_seed}")