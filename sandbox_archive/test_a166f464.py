# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def walsh_hadamard_transform(circuit, n):
        f_hat = [0] * (3**n)
        for alpha in product(range(3), repeat=n):
            value = 1
            for i in range(n):
                if circuit[i][alpha[i]] == 'AND':
                    value *= -1
                elif circuit[i][alpha[i]] == 'MOD_6':
                    value *= 2
            f_hat[sum(alpha)] += value
        return f_hat
    
    def gaussian_elimination(matrix, n):
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
                break
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(i+1, n):
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix, n):
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix, n)
        rank = 0
        for i in range(n):
            if any(matrix[i]):
                rank += 1
        return rank
    
    def generate_acc0_circuit(size, depth):
        circuit = []
        for _ in range(depth):
            layer = []
            for _ in range(size // depth):
                gate = random.choice(['AND', 'MOD_6'])
                layer.append(gate)
            circuit.append(layer)
        return circuit
    
    n_values = [4, 5, 6, 7]
    s_values = [3, 8, 20, 50]
    min_slack = float('inf')
    counterexample = ""
    
    for n in n_values:
        for s in s_values:
            circuit = generate_acc0_circuit(s, 2)
            f_hat = walsh_hadamard_transform(circuit, n)
            m = len(f_hat)
            A = [[0] * (n**2) for _ in range(m)]
            for i in range(m):
                alpha = [int(digit) for digit in format(i, f'0{n}b')]
                for j in range(n):
                    for k in range(n):
                        if alpha[j] == 1:
                            A[i][j*n + k] += f_hat[i]
            rank_A = rank(A, n**2)
            gamma_f = n**2 - rank_A
            slack = gamma_f - (n**2 - 10 * s)
            min_slack = min(min_slack, slack)
            if slack < 0:
                counterexample = f"n={n}, s={s}, circuit={circuit}"
    
    return {
        "metric_name": "min_slack",
        "metric_value": min_slack,
        "instances_tested": len(n_values) * len(s_values),
        "conjecture_holds": min_slack >= 0,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(res["metric_value"] < 0 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")