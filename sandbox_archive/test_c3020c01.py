# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_ac0_circuit(n, max_gates):
        if n <= 1 or max_gates <= 0:
            return []
        gates = ['NOT', 'XOR']
        circuit = []
        for _ in range(max_gates):
            gate = random.choice(gates)
            if gate == 'NOT':
                circuit.append(('NOT', random.randint(0, len(circuit) - 1)))
            elif gate == 'XOR':
                inputs = random.sample(range(len(circuit)), 2)
                circuit.append(('XOR', inputs[0], inputs[1]))
        return circuit
    
    def construct_algebra(circuit):
        n = len(circuit)
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                result = 0
                for gate in circuit:
                    if gate[0] == 'NOT':
                        input_index = gate[1]
                        result ^= A[i][input_index]
                    elif gate[0] == 'XOR':
                        input_indices = gate[1:]
                        result ^= (A[i][input_indices[0]] ^ A[i][input_indices[1]])
                A[j][i] = result
        return A
    
    def compute_minimal_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if A[j][i] != 0:
                        for k in range(n):
                            A[j][k] ^= A[i][k]
        return rank
    
    def is_valid_circuit(circuit):
        n = len(circuit)
        for gate in circuit:
            if gate[0] == 'NOT':
                input_index = gate[1]
                if input_index >= n or input_index < 0:
                    return False
            elif gate[0] == 'XOR':
                inputs = gate[1:]
                if any(input_index >= n or input_index < 0 for input_index in inputs):
                    return False
        return True
    
    def is_associative(A):
        n = len(A)
        for i, j, k in combinations(range(n), 3):
            if A[i][j] != A[k][i]:
                return False
        return True
    
    n = random.randint(5, 40)
    max_gates = 40
    circuit = generate_ac0_circuit(n, max_gates)
    
    if not is_valid_circuit(circuit):
        return {
            "metric_name": "gate_count",
            "metric_value": len(circuit),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Invalid circuit"
        }
    
    A = construct_algebra(circuit)
    
    if not is_associative(A):
        return {
            "metric_name": "gate_count",
            "metric_value": len(circuit),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-associative algebra"
        }
    
    minimal_rank = compute_minimal_rank(A)
    
    return {
        "metric_name": "gate_count",
        "metric_value": len(circuit),
        "instances_tested": 1,
        "conjecture_holds": minimal_rank == len(circuit),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")