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
    
    def generate_ac0_circuit(n):
        # Generate a random AC⁰ circuit with n inputs
        circuit = []
        for _ in range(random.randint(1, 5)):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                gate = [random.choice([f'x{i}' for i in range(n)]) for _ in range(2)]
            else:
                gate = [random.choice([f'x{i}' for i in range(n)]) for _ in range(2)]
            circuit.append((gate_type, gate))
        return circuit
    
    def tropical_rank(circuit):
        # Convert the circuit to a matrix and compute its rank
        n = len(circuit)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            matrix[i][i] = -math.inf
        for gate_type, gate in circuit:
            if gate_type == 'AND':
                a, b = gate
                matrix[ord(a[1:]) - ord('x'), n] = max(matrix[ord(a[1:]) - ord('x'), n], 0)
                matrix[ord(b[1:]) - ord('x'), n] = max(matrix[ord(b[1:]) - ord('x'), n], 0)
            else:
                a, b = gate
                matrix[ord(a[1:]) - ord('x'), n] = max(matrix[ord(a[1:]) - ord('x'), n], 0)
                matrix[ord(b[1:]) - ord('x'), n] = max(matrix[ord(b[1:]) - ord('x'), n], 0)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n + 1)):
                rank += 1
        return rank
    
    def log_size(circuit):
        # Calculate the size of the circuit
        size = 0
        for gate_type, gate in circuit:
            size += len(gate)
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_ac0_circuit(n)
            rank = tropical_rank(circuit)
            size = log_size(circuit)
            if size == 0:
                continue
            results.append((rank, size))
    
    total_rank = sum(rank for rank, size in results)
    total_size = sum(size for rank, size in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for rank, size in results) / len(results))
    
    conjecture_holds = all(rank >= 0.5 * math.log(size) for rank, size in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")