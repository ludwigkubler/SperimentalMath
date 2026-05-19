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
    
    def generate_circuit(n, s):
        circuit = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR', 'NOT', 'MOD_2'])
            if gate_type == 'NOT':
                circuit.append((gate_type, random.randint(0, n-1)))
            else:
                inputs = [random.randint(0, n-1) for _ in range(random.randint(1, 3))]
                circuit.append((gate_type, inputs))
        return circuit
    
    def simulate_circuit(circuit, n):
        stack = [i for i in range(n)]
        for gate in circuit:
            if gate[0] == 'NOT':
                a = stack.pop()
                stack.append(1 - a)
            elif gate[0] == 'AND':
                a, b = stack.pop(), stack.pop()
                stack.append(a & b)
            elif gate[0] == 'OR':
                a, b = stack.pop(), stack.pop()
                stack.append(a | b)
            else:  # MOD_2
                a, b = stack.pop(), stack.pop()
                stack.append((a + b) % 2)
        return stack[0]
    
    def estimate_bias(circuit, n):
        N = 2048
        count = 0
        for _ in range(N):
            result = simulate_circuit(circuit, n)
            if result == 1:
                count += 1
        bias = Fraction(count, N)
        return bias
    
    def count_saw_walks(G, L, start):
        visited = set()
        stack = [(start, [start])]
        count = 0
        while stack:
            node, path = stack.pop()
            if len(path) == L:
                count += 1
            else:
                for neighbor in G[node]:
                    if neighbor not in path:
                        stack.append((neighbor, path + [neighbor]))
        return count
    
    def build_graph(circuit):
        n = len(circuit)
        G = [[] for _ in range(n)]
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'NOT':
                G[inputs].append(i)
            else:
                for input_ in inputs:
                    G[input_].append(i)
        return G
    
    n_values = [8, 10, 12, 14, 16]
    s_values = [12, 16, 20, 24, 28, 32, 36, 40]
    for n in n_values:
        for s in s_values:
            circuit = generate_circuit(n, s)
            bias = estimate_bias(circuit, n)
            if abs(bias - Fraction(1, 3)) < Fraction(1, 9):
                G = build_graph(circuit)
                L = math.floor(2 * math.log2(s + 2))
                if L > 14:
                    L = 14
                c_L = count_saw_walks(G, L, n - 1)
                rho = math.log2(c_L + 1) / L
                if rho < (1/8) * math.log2(s) - 1:
                    return {
                        "metric_name": "SAW connective growth",
                        "metric_value": rho,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"rho={rho} < (1/8)*log2({s})-1"
                    }
    return {
        "metric_name": "SAW connective growth",
        "metric_value": None,
        "instances_tested": 0,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")