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

def generate_circuit(n, s):
    circuit = []
    for _ in range(s):
        gate_type = random.choice(['AND', 'OR', 'NOT'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, n-1)]
        else:
            inputs = [random.randint(0, n-1) for _ in range(2)]
        circuit.append((gate_type, inputs))
    return circuit

def simulate_circuit(circuit, n):
    stack = []
    input_values = {i: random.choice([0, 1]) for i in range(n)}
    
    for gate in circuit:
        if gate[0] == 'NOT':
            a = stack.pop()
            stack.append(1 - a)
        elif gate[0] == 'AND':
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        else:  # OR
            b, a = stack.pop(), stack.pop()
            stack.append(a + b - a * b)
    
    return stack[-1]

def estimate_bias(circuit, n):
    N = 2048
    count_mod_3 = 0
    
    for _ in range(N):
        result = simulate_circuit(circuit, n)
        if result % 3 == 0:
            count_mod_3 += 1
    
    bias = Fraction(count_mod_3, N)
    return bias

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14, 16]
    s_values = [12, 16, 20, 24, 28, 32, 36, 40]
    L_max = 14
    
    for n in n_values:
        for s in s_values:
            circuit = generate_circuit(n, s)
            bias = estimate_bias(circuit, n)
            
            if abs(bias - Fraction(1, 3)) < Fraction(1, 9):
                L = min(L_max, math.floor(2 * math.log2(s + 2)))
                
                def dfs(node, path, visited):
                    nonlocal c_L
                    if len(path) == L:
                        c_L += 1
                        return
                    for neighbor in G[node]:
                        if neighbor not in visited:
                            dfs(neighbor, path + [neighbor], visited | {node})
                
                G = [[] for _ in range(s)]
                for gate_type, inputs in circuit:
                    if gate_type == 'NOT':
                        G[inputs[0]].append(s)
                    else:
                        for input in inputs:
                            G[input].append(s)
                
                c_L = 0
                dfs(s - 1, [s - 1], {s - 1})
                
                rho_C = math.log2(c_L + 1) / L
                
                if rho_C < (1/8) * math.log2(s) - 1:
                    return {
                        "metric_name": "rho_C",
                        "metric_value": rho_C,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, s={s}, rho_C={rho_C}"
                    }
    
    return {
        "metric_name": "rho_C",
        "metric_value": None,
        "instances_tested": 0,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho_C = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = len([result for result in results if result["instances_tested"] > 0]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho_C} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")