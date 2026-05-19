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
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate in circuit:
            if isinstance(gate, tuple):  # Input literal
                stack.append(gate[1])
            else:  # Gate operation
                b = stack.pop()
                a = stack.pop()
                if gate == 'AND':
                    stack.append(a and b)
                elif gate == 'OR':
                    stack.append(a or b)
                elif gate == 'NOT':
                    stack.append(not b)
        return stack[0]
    
    def estimate_p_g(g, n):
        N = min(2**n, 16384)
        count = sum(evaluate_circuit(circuit, [random.randint(0, 1) for _ in range(n)]) for _ in range(N))
        p_g = Fraction(count, N)
        return p_g
    
    def psi(C):
        m = len(C)
        total = 0
        for g in C:
            p_g = estimate_p_g(g, n)
            min_p_g = min(p_g, 1 - p_g)
            max_min_p_g = max(min_p_g, Fraction(1, 2 * m))
            total += -math.log2(2 * max_min_p_g)
        return total / m
    
    def generate_hastad_circuit(n, d):
        if d == 2:
            # Full minterm DNF
            circuit = []
            for i in range(1 << n):
                term = True
                for j in range(n):
                    if (i >> j) & 1:
                        term &= ('NOT', j)
                    else:
                        term &= ('AND', j)
                circuit.append(term)
        elif d == 3:
            # √n-block tower
            block_size = int(math.sqrt(n))
            circuit = []
            for i in range(block_size):
                for j in range(block_size):
                    if (i * block_size + j) < n:
                        circuit.append(('OR', ('AND', i), ('AND', j)))
        elif d == 4:
            # Recursive ∜n-block
            block_size = int(math.sqrt(int(math.sqrt(n))))
            circuit = []
            for i in range(block_size):
                for j in range(block_size):
                    for k in range(block_size):
                        if (i * block_size**2 + j * block_size + k) < n:
                            circuit.append(('OR', ('AND', i), ('AND', j), ('AND', k)))
        return circuit
    
    def generate_random_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            if gate_type == 'NOT':
                inputs = [inputs[0]]
            circuit.append((gate_type,) + tuple(inputs))
        return circuit
    
    def generate_or_circuit(n):
        return [('OR',)] * n
    
    # Parameters
    n_values = [6, 8, 10, 12, 16, 20, 24, 30]
    d_values = [2, 3, 4]
    
    results = []
    for n in n_values:
        for d in d_values:
            # Håstad-style depth-d AC⁰ PARITY circuit
            circuit = generate_hastad_circuit(n, d)
            psi_value = psi(circuit)
            if psi_value > math.log2(len(circuit)) + 1:
                return {
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": len(circuit),
                    "conjecture_holds": False,
                    "counterexample": f"Håstad-style depth-{d} circuit with n={n}"
                }
            results.append({"psi": psi_value, "n": n, "d": d})
            
            # AC⁰ circuits of matching size computing random non-PARITY functions
            circuit = generate_random_circuit(n, len(circuit))
            psi_value = psi(circuit)
            if psi_value > math.log2(len(circuit)) + 1:
                return {
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": len(circuit),
                    "conjecture_holds": False,
                    "counterexample": f"Random AC⁰ circuit with n={n}"
                }
            results.append({"psi": psi_value, "n": n, "d": d})
            
            # Tiny AC⁰ computing the OR_n function
            circuit = generate_or_circuit(n)
            psi_value = psi(circuit)
            if psi_value > math.log2(len(circuit)) + 1:
                return {
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": len(circuit),
                    "conjecture_holds": False,
                    "counterexample": f"OR_n circuit with n={n}"
                }
            results.append({"psi": psi_value, "n": n, "d": d})
    
    # Compute statistics
    mean_psi = sum(result["psi"] for result in results) / len(results)
    std_psi = math.sqrt(sum((result["psi"] - mean_psi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["psi"] <= math.log2(len(result["circuit"])) + 1) / len(results)
    
    return {
        "metric_name": "psi",
        "metric_value": mean_psi,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_psi = sum(result["metric_value"] for result in results) / len(results)
    std_psi = math.sqrt(sum((result["metric_value"] - mean_psi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_psi} std={std_psi} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")