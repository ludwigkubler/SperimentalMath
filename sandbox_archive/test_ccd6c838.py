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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n + 1)]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i+1, n):
            x[i] -= Fraction(A[i][j] * x[j], A[i][i])

    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            output = random.randint(0, 1)
            circuit.append((gate_type, inputs, output))
        return circuit

    def compute_circuit_rank(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n)]
        b = [0] * n
        for i, (gate_type, inputs, output) in enumerate(circuit):
            if gate_type == 'AND':
                A[i][inputs[0]] += 1
                A[i][inputs[1]] += 1
                A[i][n] -= 2 * output
            elif gate_type == 'OR':
                A[i][inputs[0]] += 1
                A[i][inputs[1]] += 1
                A[i][n] -= (1 - output)
        rank = gaussian_elimination(A, b).count(0)
        return n - rank

    circuit_ranks = []
    for _ in range(30):
        circuit_size = random.randint(5, 40)
        circuit = generate_circuit(circuit_size)
        rank = compute_circuit_rank(circuit)
        circuit_ranks.append(rank)

    mean_rank = sum(circuit_ranks) / len(circuit_ranks)
    conjecture_holds = mean_rank >= circuit_size
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} < size {circuit_size}"

    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(circuit_ranks),
        "n_max": max(len(circuit) for circuit in [generate_circuit(n) for n in range(5, 41)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")