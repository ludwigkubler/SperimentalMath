# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_circuit(n, s):
    depth = 3
    circuit = []
    for _ in range(depth):
        layer = []
        for _ in range(s // depth):
            if _ % 2 == 0:
                gate_type = 'AND'
            else:
                gate_type = 'OR'
            layer.append(gate_type)
        circuit.extend(layer)
    return circuit

def simulate_circuit(circuit, n):
    stack = []
    for gate in circuit:
        if gate == 'NOT':
            a = stack.pop()
            stack.append(not a)
        elif gate == 'AND':
            b, a = stack.pop(), stack.pop()
            stack.append(a and b)
        elif gate == 'OR':
            b, a = stack.pop(), stack.pop()
            stack.append(a or b)
    return stack[0]

def estimate_bias(circuit, n):
    N = 2048
    count = 0
    for _ in range(N):
        result = simulate_circuit(circuit, n)
        if result % 3 == 1:
            count += 1
    bias = count / N
    return bias

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14, 16]
    s_values = [12, 16, 20, 24, 28, 32, 36, 40]
    L_max = 14
    
    results = []
    for n in n_values:
        for s in s_values:
            circuit = generate_circuit(n, s)
            bias = estimate_bias(circuit, n)
            if abs(bias - 1/3) >= 1/9:
                L = math.floor(2 * math.log2(s + 2))
                if L > L_max:
                    continue
                c_L = 0
                visited = [False] * (s + 1)
                stack = [(s, [])]
                while stack:
                    node, path = stack.pop()
                    if len(path) == L and node == s:
                        c_L += 1
                        continue
                    for i in range(s):
                        if not visited[i]:
                            visited[i] = True
                            stack.append((i, path + [i]))
                            visited[i] = False
                rho = math.log2(c_L + 1) / L
                results.append({
                    "n": n,
                    "s": s,
                    "bias": bias,
                    "rho": rho,
                    "c_L": c_L,
                    "L": L
                })
    
    if not results:
        return {
            "metric_name": "rho",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No biased circuits found"
        }
    
    rho_values = [result["rho"] for result in results]
    bias_values = [result["bias"] for result in results]
    n_tests = len(results)
    
    if all(rho >= (1/8) * math.log2(s) - 1 for s, _, rho in results):
        return {
            "metric_name": "rho",
            "metric_value": sum(rho_values) / n_tests,
            "instances_tested": n_tests,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"Counterexample found with bias={max(bias_values)} and rho={min(rho_values)}"
        return {
            "metric_name": "rho",
            "metric_value": sum(rho_values) / n_tests,
            "instances_tested": n_tests,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    rho_values = [result["metric_value"] for result in results if "metric_value" in result]
    instances_tested = sum(result["instances_tested"] for result in results if "instances_tested" in result)
    support_fraction = sum(1 for result in results if result.get("conjecture_holds", False)) / len(results)
    
    if all(rho >= (1/8) * math.log2(s) - 1 for s, _, rho in results):
        print(f"RESULT: SUPPORTED mean={sum(rho_values)/instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not result.get("conjecture_holds", False) for result in results):
        counterexample = next(result["counterexample"] for result in results if not result.get("conjecture_holds", False))
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result.get("conjecture_holds", False))
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")