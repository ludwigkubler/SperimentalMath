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
    
    def generate_xor_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def quandle_representation(circuit):
        n = len(circuit)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                Q[i][i] = 1
                for j in inputs:
                    Q[j][i] = 1
            elif gate_type == 'OR':
                Q[i][i] = 1
                for j in inputs:
                    Q[i][j] = 1
        return Q
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def compute_minimal_rank(circuit):
        Q = quandle_representation(circuit)
        return gaussian_elimination(Q)
    
    n_values = [10, 20, 30, 40]
    ranks = []
    for n in n_values:
        circuits = [generate_xor_circuit(n) for _ in range(30)]
        for circuit in circuits:
            rank = compute_minimal_rank(circuit)
            if rank < n ** 0.5:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": len(ranks),
                    "conjecture_holds": False,
                    "counterexample": f"XOR circuit with n={n} gates has minimal rank {rank} < {n ** 0.5}"
                }
            ranks.append(rank)
    
    avg_rank = sum(ranks) / len(ranks)
    std_dev = math.sqrt(sum((x - avg_rank) ** 2 for x in ranks) / len(ranks))
    support_fraction = sum(1 for rank in ranks if abs(rank - n_values[0] ** 0.5) <= 0.3 * n_values[0] ** 0.5 and std_dev <= 0.1 * n_values[0] ** 0.5)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": support_fraction / len(ranks) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if support_fraction == len(seeds):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8 * len(seeds):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal rank < n^(1/2)\" first_failing_seed={first_failing_seed}")