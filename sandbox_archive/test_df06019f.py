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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                return None  # Singular matrix, no unique solution
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return A

    def minimal_order(A):
        A = gaussian_elimination(A)
        if A is None:
            return None
        rank = sum(1 for row in A if any(row))
        return rank

    def circuit_weight(circuit):
        # Simplified weight calculation based on circuit structure
        return len(circuit)

    def generate_circuit(size):
        # Generate a random boolean circuit of the given size
        circuit = []
        for _ in range(size):
            gate = random.choice(['AND', 'OR', 'NOT'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate, inputs))
        return circuit

    def matrix_from_circuit(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n)]
        for i, (gate, inputs) in enumerate(circuit):
            if gate == 'AND':
                for j in inputs:
                    A[i][j] += 1
            elif gate == 'OR':
                for j in inputs:
                    A[i][n] += 1
            else:  # NOT
                A[i][inputs[0]] = -1
        return A

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)

    def mean_absolute_deviation(values, target):
        return sum(abs(v - target) for v in values) / len(values)

    sizes = [5, 10, 15, 20, 30, 40]
    orders = []
    weights = []

    for size in sizes:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(size)
            A = matrix_from_circuit(circuit)
            order = minimal_order(A)
            if order is not None:
                orders.append(order)
                weights.append(circuit_weight(circuit))

    correlation_coefficient = pearson_correlation(orders, weights)
    mean_order = sum(orders) / len(orders)
    mean_deviation = mean_absolute_deviation(orders, mean_order)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(orders),
        "n_max": max(sizes),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_deviation <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_deviation <= 3 else "Pearson Correlation Coefficient < 0.8 or Mean Absolute Deviation > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation Coefficient < 0.8 or Mean Absolute Deviation > 3\" first_failing_seed={first_failing_seed}")