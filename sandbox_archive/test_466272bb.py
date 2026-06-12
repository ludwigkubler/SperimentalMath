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
    
    def gaussian_elimination(A, mod):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                if j != i:
                    factor = (A[j][i] * pow(pivot, mod-2, mod)) % mod
                    for k in range(n):
                        A[j][k] = (A[j][k] - factor * A[i][k]) % mod
        return A
    
    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_power(A, k, mod):
        n = len(A)
        result = [[0]*n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        while k > 0:
            if k % 2 == 1:
                result = matrix_mult(result, A, mod)
            A = matrix_mult(A, A, mod)
            k //= 2
        return result
    
    def symplectic_invariant(circuit):
        n = len(circuit)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i][j] == 'X':
                    A[i][j] = 1
                    A[j][i] = 1
        A = gaussian_elimination(A, 2)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i][j] == 'CNOT':
                    count += 1
        return count
    
    def generate_circuit(n):
        circuit = [['I']*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    circuit[i][j] = 'X'
                    circuit[j][i] = 'X'
        for i in range(n):
            for j in range(n):
                if i != j and random.choice([True, False]):
                    circuit[i][j] = 'CNOT'
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_shv = 0
        total_ec = 0
        
        while len(results) < 30:
            circuit = generate_circuit(n)
            shv = symplectic_invariant(circuit)
            ec = entanglement_complexity(circuit)
            
            if shv > 0 and ec > 0:
                results.append((shv, ec))
                total_shv += shv
                total_ec += ec
                instances_tested += 1
        
        mean_shv = total_shv / len(results)
        mean_ec = total_ec / len(results)
        
        if len(results) < 30:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        correlation_coefficient = (sum((shv - mean_shv) * (ec - mean_ec) for shv, ec in results) /
                                   math.sqrt(sum((shv - mean_shv)**2 for shv, _ in results) *
                                             sum((ec - mean_ec)**2 for _, ec in results)))
        
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": abs(correlation_coefficient) >= 0.95,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result["metric_value"])
    
    mean_shv = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_shv)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) >= 0.95) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_shv} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r) < 0.95 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.95))]
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")