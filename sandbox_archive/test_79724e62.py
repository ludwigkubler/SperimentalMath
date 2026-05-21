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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def continued_fraction_length(p, q):
    if q == 0:
        return 0
    r = p % q
    return 1 + continued_fraction_length(q, r)

def build_random_circuit(n, size, depth):
    circuit = []
    gates = ['AND', 'OR', 'MOD_2', 'MOD_3', 'NOT']
    
    def add_gate(gate_type):
        if len(circuit) < size:
            input_indices = [random.randint(0, len(circuit) - 1) for _ in range(3)]
            circuit.append((gate_type, input_indices))
    
    for _ in range(depth):
        gate_type = random.choice(gates)
        add_gate(gate_type)
    
    return circuit

def evaluate_circuit(circuit, n):
    truth_table = [[0] * (2 ** n) for _ in range(2 ** n)]
    
    def eval_gate(gate, inputs):
        if gate[0] == 'AND':
            return all(truth_table[i][j] & truth_table[j][k] for i, j, k in zip(inputs, inputs[1:], inputs[2:]))
        elif gate[0] == 'OR':
            return any(truth_table[i][j] | truth_table[j][k] for i, j, k in zip(inputs, inputs[1:], inputs[2:]))
        elif gate[0] == 'MOD_2':
            return sum(truth_table[i][j] for i, j in zip(inputs, inputs[1:])) % 2
        elif gate[0] == 'MOD_3':
            return sum(truth_table[i][j] for i, j in zip(inputs, inputs[1:])) % 3
        elif gate[0] == 'NOT':
            return not truth_table[inputs[0]][inputs[1]]
    
    def eval_row(row):
        if len(row) == 1:
            return row[0]
        else:
            return eval_gate(circuit[row[-2]], [eval_row(row[:i]) for i in range(1, len(row))])
    
    for x in range(2 ** n):
        truth_table[x][x] = eval_row(list(range(n)))
    
    return truth_table

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 15, 18]
    size_values = [20, 40, 80]
    depth_values = [2, 3, 4]
    
    metrics = []
    
    for n in n_values:
        for size in size_values:
            for depth in depth_values:
                circuit = build_random_circuit(n, size, depth)
                truth_table = evaluate_circuit(circuit, n)
                
                p_i, q_i = 0.5, 1
                trajectory = []
                
                for _ in range(math.ceil(math.log2(n))):
                    max_diff = -1
                    best_var_val = None
                    
                    for var in range(n):
                        for val in [0, 1]:
                            new_p_i = sum(truth_table[i][var] * (val if i & (1 << var) else 1 - val) for i in range(2 ** n)) / 2 ** n
                            diff = abs(new_p_i - 0.5)
                            if diff > max_diff:
                                max_diff = diff
                                best_var_val = (var, val)
                    
                    p_i, q_i = new_p_i, q_i * 2
                    trajectory.append((p_i, q_i))
                
                D_f = sum(continued_fraction_length(p, q) for p, q in trajectory)
                metrics.append(D_f)
    
    if not metrics:
        return {
            "metric_name": "D(f)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_D = sum(metrics) / len(metrics)
    std_D = (sum((x - mean_D) ** 2 for x in metrics) / len(metrics)) ** 0.5
    support_fraction = sum(1 for D in metrics if D <= 8 * depth_values[0] * (math.log2(size_values[0]))**2 + depth_values[0] * math.log2(n_values[0])) / len(metrics)
    
    return {
        "metric_name": "D(f)",
        "metric_value": mean_D,
        "instances_tested": len(metrics),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_D = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_D = (sum((r["metric_value"] - mean_D) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_D} std={std_D} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")