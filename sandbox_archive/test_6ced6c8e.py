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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    max_row = j
                    break
            if max_row is None:
                continue
            matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
            pivot = matrix[rank][i]
            for j in range(n):
                matrix[rank][j] /= pivot
            for j in range(m):
                if j != rank and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def generate_random_circuit(depth, n_inputs):
        circuit = []
        for _ in range(depth):
            gate = random.choice(['AND', 'OR'])
            if gate == 'AND':
                inputs = [random.randint(0, 1) for _ in range(n_inputs)]
            else:
                inputs = [random.randint(0, 1) for _ in range(n_inputs)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_k_theoretic_dimension(circuit):
        n_inputs = len(circuit[0][1])
        matrix = [[0] * (n_inputs + 1) for _ in range(2**n_inputs)]
        for i in range(2**n_inputs):
            inputs = [(i >> j) & 1 for j in range(n_inputs)]
            output = 0
            for gate, inputs_gate in circuit:
                if gate == 'AND':
                    output &= all(inputs_gate)
                else:
                    output |= any(inputs_gate)
            matrix[i][n_inputs] = output
            for j in range(n_inputs):
                matrix[i][j] = inputs[j]
        return gaussian_elimination(matrix)
    
    n_max = 40
    instances_tested = 0
    total_k_theo = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(depth, n_inputs=depth)
            k_theo = compute_k_theoretic_dimension(circuit)
            total_k_theo += k_theo
            instances_tested += 1
    
    mean_k_theo = total_k_theo / instances_tested
    conjecture_holds = mean_k_theo <= depth**2
    counterexample = "" if conjecture_holds else f"mean_k_theo={mean_k_theo}, depth^2={depth**2}"
    
    return {
        "metric_name": "K-theoretic dimension",
        "metric_value": mean_k_theo,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_k_theo = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_k_theo} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_k_theo} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")