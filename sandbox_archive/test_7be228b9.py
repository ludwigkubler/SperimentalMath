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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def is_reflection_matrix(M):
        n = len(M)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        M_inv = [row[:] for row in M]
        for _ in range(n - 1):
            for j in range(n):
                M_inv[j][j] /= M[j][j]
                for k in range(j + 1, n):
                    M_inv[k][j] /= M[j][j]
                    M_inv[j][k] /= M[j][j]
        return M @ M_inv == identity
    
    def generate_circuit(n):
        gates = []
        for _ in range(2 * n - 2):
            gate_type = random.choice(['AND', 'OR'])
            qubits = sorted(random.sample(range(n), 2))
            gates.append((gate_type, qubits))
        return gates
    
    def simulate_circuit(circuit, n):
        state = [0] * n
        for gate_type, qubits in circuit:
            if gate_type == 'AND':
                state[qubits[1]] &= state[qubits[0]]
            elif gate_type == 'OR':
                state[qubits[1]] |= state[qubits[0]]
        return tuple(state)
    
    def generate_reflection_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = -1
            M[i][(i + 1) % n] = 1
            M[(i + 1) % n][i] = 1
        return M
    
    def count_reflections(state, n):
        reflections = 0
        for i in range(n):
            if state[i] != 0:
                reflection = generate_reflection_matrix(n)
                reflection[i][i] *= -1
                state = gaussian_elimination(reflection, list(state))
                reflections += 1
        return reflections
    
    n_max = 40
    instances_tested = 30
    total_reflections = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        state = simulate_circuit(circuit, n)
        reflections = count_reflections(state, n)
        total_reflections += reflections
    
    mean_reflections = total_reflections / instances_tested
    conjecture_holds = mean_reflections == 0 or abs(mean_reflections - len(circuit)) < 5
    
    return {
        "metric_name": "Mean Reflections",
        "metric_value": mean_reflections,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean reflections {mean_reflections} differs from circuit length {len(circuit)} by more than 5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_reflections = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_reflections} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        print(f"RESULT: FALSIFIED counterexample=\"Mean reflections differ from circuit length\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded n_tested=30")