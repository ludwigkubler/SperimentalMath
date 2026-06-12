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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2 * n):
            gate = random.choice(['H', 'CNOT'])
            qubit1 = random.randint(0, n - 1)
            qubit2 = random.randint(0, n - 1)
            if gate == 'CNOT' and qubit1 == qubit2:
                continue
            circuit.append((gate, qubit1, qubit2))
        return circuit
    
    def matrix_mult(A, B, mod):
        m = len(A)
        p = len(B[0])
        result = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(len(B)):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
        return result
    
    def symplectic_invariant(circuit):
        n = len(circuit) // 2 + 1
        identity = [[0 if i != j else 1 for j in range(2 * n)] for i in range(2 * n)]
        CNOT = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]
        
        invariant = identity
        for gate, qubit1, qubit2 in circuit:
            if gate == 'H':
                H = [
                    [1, 1],
                    [1, -1]
                ]
                H[0][1] %= n
                H[1][1] %= n
                invariant = matrix_mult(invariant, H, n)
            elif gate == 'CNOT':
                CNOT[2][3] = (CNOT[2][3] + 1) % n
                CNOT[3][2] = (CNOT[3][2] + 1) % n
                invariant = matrix_mult(invariant, CNOT, n)
        
        return sum(sum(row) for row in invariant) % n
    
    def entanglement_complexity(circuit):
        complexity = 0
        qubits_used = set()
        for gate, qubit1, qubit2 in circuit:
            if gate == 'CNOT':
                qubits_used.add(qubit1)
                qubits_used.add(qubit2)
        return len(qubits_used) - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            order = symplectic_invariant(circuit)
            complexity = entanglement_complexity(circuit)
            results.append((n, order, complexity))
    
    if not results:
        return {
            "metric_name": "symplectic_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "symplectic_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    orders = [order for _, order, _ in results]
    complexities = [complexity for _, _, complexity in results]
    
    mean_order = sum(orders) / len(orders)
    std_order = math.sqrt(sum((x - mean_order) ** 2 for x in orders) / len(orders))
    correlation = sum((orders[i] - mean_order) * (complexities[i] - mean_complexity) for i in range(len(results))) / (len(results) * std_order * std_complexity)
    
    return {
        "metric_name": "symplectic_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")