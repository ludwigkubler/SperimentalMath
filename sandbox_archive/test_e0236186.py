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
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(len(left) + len(right))]

    def state_space_representation(circuit):
        if not circuit:
            return []
        elif len(circuit) == 1:
            return [[circuit[0]], [1 - circuit[0]]]
        else:
            left = state_space_representation(circuit[:len(circuit)//2])
            right = state_space_representation(circuit[len(circuit)//2:])
            return [[l, r] for l in left for r in right]

    def minimal_polynomial(state_space):
        n = len(state_space)
        if n == 1:
            return [state_space[0][0]]
        else:
            A = []
            for i in range(n):
                row = []
                for j in range(n):
                    if state_space[i][j] != state_space[j][i]:
                        row.append(1)
                    else:
                        row.append(0)
                A.append(row)
            return gaussian_elimination(A)

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return [row[n-1] for row in matrix]

    def topological_entropy(state_space):
        n = len(state_space)
        if n == 1:
            return 0
        else:
            A = []
            for i in range(n):
                row = []
                for j in range(n):
                    if state_space[i][j] != state_space[j][i]:
                        row.append(1)
                    else:
                        row.append(0)
                A.append(row)
            return -sum(sum(abs(x) * math.log2(abs(x)) for x in row) for row in A) / n

    def depth(circuit):
        if not circuit:
            return 0
        elif len(circuit) == 1:
            return 1
        else:
            left = depth(circuit[:len(circuit)//2])
            right = depth(circuit[len(circuit)//2:])
            return max(left, right) + 1

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            state_space = state_space_representation(circuit)
            m = depth(circuit)
            H_C = topological_entropy(state_space)
            log_m = math.log2(m) if m > 0 else float('inf')
            metrics.append((H_C, log_m))

    metric_values = [metric[0] for metric in metrics]
    log_m_values = [metric[1] for metric in metrics]

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(metric_values, log_m_values)) / len(metrics)
    mean_x = sum(metric_values) / len(metric_values)
    mean_y = sum(log_m_values) / len(log_m_values)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) >= 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{abs(result['metric_value'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")