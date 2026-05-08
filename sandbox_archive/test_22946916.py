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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count=30):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_ac0_circuit(n, depth):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_ac0_circuit(n // 2, depth - 1) for _ in range(2)]
            return [subcircuits[0][i] ^ subcircuits[1][i] for i in range(n)]
    
    def communication_matrix(circuit):
        n = len(circuit)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if circuit[i] == circuit[j]:
                    M[i][j] = 1
        return M
    
    def hadamard_transform(M):
        n = len(M)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                H[i][j] = (1 / math.sqrt(n)) * (-1) ** ((i & j).bit_count() % 2)
        return matrix_multiply(H, matrix_multiply(M, H))
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def discrepancy(M):
        n = len(M)
        max_diff = 0
        for i in range(n):
            for j in range(n):
                diff = abs(sum(M[i]) - sum(M[j]))
                if diff > max_diff:
                    max_diff = diff
        return max_diff
    
    def size(circuit):
        if isinstance(circuit, list):
            return sum(size(subcircuit) for subcircuit in circuit)
        else:
            return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 circuits per n
            circuit = generate_ac0_circuit(n, random.randint(1, 3))
            M_C = communication_matrix(circuit)
            disc_M_C = discrepancy(M_C)
            size_C = size(circuit)
            log_size_C = math.log(size_C)
            total_metric_value += disc_M_C / log_size_C
            instances_tested += 1
            if disc_M_C < log_size_C:
                conjecture_holds = False
                counterexample = f"n={n}, circuit_size={size_C}, discrepancy={disc_M_C}, expected>=log({size_C})"
    
    return {
        "metric_name": "discrepancy/log(size(C))",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes()
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")