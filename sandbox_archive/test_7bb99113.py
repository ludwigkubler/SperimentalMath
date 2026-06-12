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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0'] * 2
        else:
            subcircuits = [generate_boolean_circuit(depth - 1) for _ in range(2)]
            return ['&', '|'] + sum(subcircuits, [])
    
    def evaluate_circuit(circuit):
        stack = []
        for token in reversed(circuit):
            if token == '0' or token == '1':
                stack.append(int(token))
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(a & b if token == '&' else a | b)
        return stack[0]
    
    def matrix_multiply(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def matrix_power(M, k, mod):
        n = len(M)
        result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, M, mod)
            M = matrix_multiply(M, M, mod)
            k //= 2
        return result
    
    def minimal_brauer_group_order(circuit):
        n = len(circuit) + 1
        mod = 10**9 + 7
        A = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            if circuit[i] == '&':
                A[0][i + 1] = 1
                A[i + 1][n - 1] = 1
            elif circuit[i] == '|':
                A[0][i + 1] = 1
                A[n - 2][i + 1] = 1
        return matrix_power(A, n - 1, mod)[0][n - 1]
    
    def circuit_depth(circuit):
        if isinstance(circuit, list):
            return max(circuit_depth(subcircuit) for subcircuit in circuit) + 1
        else:
            return 0
    
    depths = [5, 10]
    results = []
    for depth in depths:
        for _ in range(30):
            circuit = generate_boolean_circuit(depth)
            depth_val = circuit_depth(circuit)
            br_order = minimal_brauer_group_order(circuit)
            if depth_val == 0 or br_order == 0:
                continue
            results.append((depth_val, br_order))
    
    if not results:
        return {
            "metric_name": "Brauer Group Order / Circuit Depth Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 10,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [br_order / depth for depth, br_order in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    return {
        "metric_name": "Brauer Group Order / Circuit Depth Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(depth for depth, _ in results),
        "conjecture_holds": all(0.7 * mean_ratio <= ratio <= 1.3 * mean_ratio for ratio in ratios),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std={std_ratio:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")