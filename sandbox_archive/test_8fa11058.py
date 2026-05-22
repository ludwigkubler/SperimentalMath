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
    
    def generate_ac0_parity_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['XOR', 'NOT'])
            if gate == 'XOR':
                circuit.append('XOR')
                circuit.append(random.choice([True, False]))
            else:
                circuit.append('NOT')
        return circuit
    
    def evaluate_circuit(circuit, input_bits):
        result = input_bits[0]
        for i in range(1, len(circuit)):
            if circuit[i] == 'XOR':
                result ^= input_bits[i]
            elif circuit[i]:
                result = not result
        return result
    
    def polynomial_from_circuit(circuit):
        n = len(circuit)
        poly = [0] * (n + 1)
        for i in range(n):
            if circuit[i] == 'XOR':
                poly[1] += input_bits[i]
            elif circuit[i]:
                poly[1] -= input_bits[i]
        return poly
    
    def norm(poly):
        return sum(x**2 for x in poly) ** 0.5
    
    def quaternionic_embedding(poly):
        n = len(poly)
        Q = [[0, 0], [0, 0]]
        for i in range(n + 1):
            Q[0][0] += poly[i]
            Q[1][1] -= poly[i]
        return Q
    
    def isometric_embedding(Q1, Q2):
        n = len(Q1)
        for i in range(n):
            for j in range(n):
                if not (Q1[i][j] == Q2[i][j]):
                    return False
        return True
    
    def find_minimal_norm(poly):
        min_norm = float('inf')
        for _ in range(100):  # Sample 100 embeddings
            Q1 = quaternionic_embedding(poly)
            Q2 = quaternionic_embedding(poly)
            while isometric_embedding(Q1, Q2):
                Q2 = quaternionic_embedding(poly)
            min_norm = min(min_norm, norm(Q1 - Q2))
        return min_norm
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_parity_circuit(n)
        input_bits = [random.choice([True, False]) for _ in range(n)]
        poly = polynomial_from_circuit(circuit)
        min_norm = find_minimal_norm(poly)
        results.append(min_norm)
    
    mean_norm = sum(results) / len(results)
    conjecture_holds = all(norm >= n**0.5 for norm, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "n-dependent"
    
    return {
        "metric_name": "Minimal Norm",
        "metric_value": mean_norm,
        "instances_tested": len(n_values),
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
    
    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n-dependent\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")