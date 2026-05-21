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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(A):
    m = len(A)
    n = len(A[0])
    reduced = gaussian_elimination(A, [0] * m)
    return sum(1 for x in reduced if any(x[j] != 0 for j in range(n)))

def generate_ac0_mod_p_circuit(n, d, s):
    gates = ['MOD_3', 'AND', 'OR', 'NOT']
    inputs = list(range(n))
    outputs = [n + i for i in range(s)]
    
    circuit = []
    for _ in range(s):
        gate_type = random.choice(gates)
        if gate_type == 'MOD_3':
            inputs_used = random.sample(inputs, 2)
            circuit.append((gate_type, inputs_used))
        elif gate_type == 'AND' or gate_type == 'OR':
            inputs_used = random.sample(inputs, 1)
            circuit.append((gate_type, inputs_used))
        elif gate_type == 'NOT':
            input_used = random.choice(inputs)
            circuit.append((gate_type, [input_used]))
    
    return circuit, outputs

def build_multigraph(circuit, outputs):
    V = set()
    E = []
    
    for gate, inputs in circuit:
        if gate == 'MOD_3':
            for _ in range(3):
                for input_node in inputs:
                    V.add(input_node)
                    E.append((input_node, gate))
        elif gate == 'AND' or gate == 'OR':
            for input_node in inputs:
                V.add(input_node)
                E.append((input_node, gate))
        elif gate == 'NOT':
            V.add(inputs[0])
            E.append((inputs[0], gate))
    
    for output in outputs:
        V.add(output)
        E.append((output, 'sink'))
    
    return V, E

def compute_epsilon(circuit, outputs):
    n = len(outputs)
    count = 0
    for x in range(2**n):
        input_bits = [int(b) for b in format(x, f'0{n}b')]
        output_bits = [circuit[i][1] if circuit[i][0] == 'NOT' else input_bits[circuit[i][1]] for i in range(len(circuit))]
        predicted_output = sum(output_bits) % 2
        actual_output = x % 2
        count += int(predicted_output == actual_output)
    return abs(count / (2**n - 0.5))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14]
    d_values = [2, 3]
    s_values = [2 * n, 4 * n, 8 * n]
    
    results = []
    for n in n_values:
        for d in d_values:
            for s in s_values:
                circuit, outputs = generate_ac0_mod_p_circuit(n, d, s)
                epsilon = compute_epsilon(circuit, outputs)
                if epsilon < 0.02:
                    continue
                
                V, E = build_multigraph(circuit, outputs)
                L_tilde = []
                for i in range(len(V) - 1):
                    row = [0] * (len(V) - 1)
                    for j in range(len(E)):
                        if E[j][0] == V[i]:
                            row[V.index(E[j][1])] += 1
                        elif E[j][1] == V[i]:
                            row[V.index(E[j][0])] -= 1
                    L_tilde.append(row)
                
                rank_L_tilde_mod_2 = rank(L_tilde)
                R = (len(V) - 1 - rank_L_tilde_mod_2) * math.log(s + 1) / (epsilon * n**(1/d))
                results.append(R)
    
    if not results:
        return {
            "metric_name": "R",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    min_R = min(results)
    median_R = sorted(results)[len(results) // 2]
    
    return {
        "metric_name": "R",
        "metric_value": R,
        "instances_tested": len(results),
        "conjecture_holds": min_R >= 0.01 and median_R >= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        mean_R = sum(results) / len(results)
        std_R = math.sqrt(sum((r - mean_R)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r >= 0.01 and r >= 0.1) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
        elif any(r < 0.01 for r in results):
            first_failing_seed = seeds[results.index(min([r for r in results if r < 0.01]))]
            print(f"RESULT: FALSIFIED counterexample=\"R<{0.01}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE not_enough_valid_instances")
    else:
        print("RESULT: INCONCLUSIVE missing_data")