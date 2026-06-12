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
    
    def generate_boolean_circuit(depth, num_inputs):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_boolean_circuit(depth - 1, num_inputs) for _ in range(2)]
            return [random.choice([0, 1]) for _ in subcircuits]
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        result = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return result
    
    def matrix_sub(A, B):
        m = len(A)
        n = len(A[0])
        result = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return result
    
    def matrix_transpose(A):
        m = len(A)
        n = len(A[0])
        result = [[A[j][i] for j in range(m)] for i in range(n)]
        return result
    
    def matrix_inverse(A, mod):
        m = len(A)
        n = len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        augmented = [row + col for row, col in zip(A, identity)]
        for i in range(m):
            pivot = augmented[i][i]
            if pivot == 0:
                raise ValueError("Matrix is not invertible")
            for j in range(n * 2):
                augmented[i][j] *= mod_inverse(pivot, mod)
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n * 2):
                        augmented[j][k] -= factor * augmented[i][k]
        inverse = [row[n:] for row in augmented]
        return inverse
    
    def mod_inverse(a, mod):
        m0, x0, x1 = mod, 0, 1
        if mod == 1:
            return 0
        while a > 1:
            q = a // mod
            m, mod, a = mod, a % mod, m - q * mod
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1
    
    def compute_brauer_group_order(circuit):
        n = len(circuit)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if circuit[i] == 1 and circuit[j] == 1:
                    A[i][j] = 1
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = matrix_add(A, I)
        det = 0
        for perm in itertools.permutations(range(n)):
            sign = 1
            for i in range(n):
                sign *= (-1) ** (perm[i] - i)
            prod = 1
            for i in range(n):
                prod *= B[perm[i]][i]
            det += sign * prod
        return abs(det) % mod
    
    def circuit_depth(circuit):
        if isinstance(circuit, list):
            return max(circuit_depth(subcircuit) for subcircuit in circuit)
        else:
            return 0
    
    mod = 10**9 + 7
    n_max = 40
    instances_tested = 0
    total_brauer_group_order = 0
    total_circuit_depth = 0
    
    for n in range(5, 41):
        for _ in range(max(30 // (n - 4), 1)):
            circuit = generate_boolean_circuit(n - 1, n)
            depth = circuit_depth(circuit)
            if depth > 10:
                continue
            instances_tested += 1
            total_brauer_group_order += compute_brauer_group_order(circuit)
            total_circuit_depth += depth
    
    if instances_tested == 0:
        return {
            "metric_name": "Brauer Group Order / Circuit Depth Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    mean_ratio = total_brauer_group_order / (total_circuit_depth * instances_tested)
    std_ratio = 0
    for i in range(instances_tested):
        circuit = generate_boolean_circuit(n - 1, n)
        depth = circuit_depth(circuit)
        if depth > 10:
            continue
        brauer_group_order = compute_brauer_group_order(circuit)
        std_ratio += (brauer_group_order / (depth * instances_tested) - mean_ratio) ** 2
    
    std_ratio /= instances_tested
    std_ratio = std_ratio**0.5
    
    support_fraction = sum(1 for _ in range(instances_tested)) / instances_tested
    
    return {
        "metric_name": "Brauer Group Order / Circuit Depth Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95 and std_ratio <= 0.3 * mean_ratio,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")