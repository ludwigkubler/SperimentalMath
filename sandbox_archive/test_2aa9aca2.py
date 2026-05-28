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

def generate_xor_circuit(n):
    circuit = []
    for _ in range(n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
        circuit.append((gate_type, inputs))
    return circuit

def quandle_representation(circuit):
    n = len(circuit)
    Q = [[0] * (n + 1) for _ in range(n + 1)]
    Q[0][0] = 1
    for i, (gate_type, inputs) in enumerate(circuit):
        if gate_type == 'AND':
            Q[i + 1][inputs[0]] = 1
            Q[i + 1][inputs[1]] = 1
            Q[i + 1][n] = -1
        elif gate_type == 'OR':
            Q[i + 1][inputs[0]] = 1
            Q[i + 1][inputs[1]] = 1
            Q[n][i + 1] = -1
    return Q

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(7):  # Aim for at least 30 instances per seed
            circuit = generate_xor_circuit(n)
            Q = quandle_representation(circuit)
            rank = gaussian_elimination(Q)
            results.append((n, rank))
    
    avg_rank = sum(rank for _, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - avg_rank) ** 2 for _, rank in results) / len(results))
    expected_avg_rank = [math.sqrt(n) for n, _ in results]
    correlation_coefficient = sum((avg_rank - e) * (rank - e) for e, rank in zip(expected_avg_rank, results)) / (len(results) * std_dev * math.sqrt(sum((e - avg_rank) ** 2 for e in expected_avg_rank)))
    
    conjecture_holds = abs(correlation_coefficient) > 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(avg_rank, std_dev, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(avg_rank, std_dev, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))