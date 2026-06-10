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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]
    
    def linear_group_representation(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (_, inputs) in enumerate(circuit):
            A[i][i] = 1
            for j in inputs:
                A[j][i] = -1
        A[n][n] = 1
        return A
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    circuit_sizes = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    n_max = 0
    
    for s in circuit_sizes:
        for _ in range(5):
            circuit = generate_circuit(s)
            rank = min_rank(linear_group_representation(circuit))
            circuit_ranks.append(rank)
            n_max = max(n_max, s)
    
    if len(circuit_ranks) < 180:  # Ensure at least 30 instances per seed
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": len(circuit_ranks),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = 0
    for i in range(len(circuit_sizes)):
        x = circuit_sizes[i]
        y = sum(circuit_ranks[j] for j in range(i * 30, (i + 1) * 30)) / 30
        correlation_coefficient += (x - 22.5) * (y - 17.5)
    correlation_coefficient /= math.sqrt(sum((x - 22.5) ** 2 for x in circuit_sizes) * sum((y - 17.5) ** 2 for y in [sum(circuit_ranks[j] for j in range(i * 30, (i + 1) * 30)) / 30 for i in range(6)]))
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuit_ranks),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")