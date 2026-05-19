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
    
    def generate_acc02_circuit(n, s):
        if n < 3 or s < 6:
            return None
        layers = []
        for _ in range(3):
            layer = [random.choice(['AND', 'OR']) for _ in range(s // 3)]
            layers.append(layer)
        circuit = sum(layers, [])
        return circuit
    
    def is_mod_3(x):
        return x % 3 == 0
    
    def simulate_circuit(circuit, n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        stack = []
        for gate in circuit:
            if gate == 'NOT':
                stack.append(1 - stack.pop())
            elif gate == 'AND':
                a = stack.pop()
                b = stack.pop()
                stack.append(a & b)
            else:  # OR
                a = stack.pop()
                b = stack.pop()
                stack.append(a | b)
        return stack[0]
    
    def count_self_avoiding_walks(G, start, L):
        visited = set()
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            if len(path) == L and G[node][node]:
                yield path
            for neighbor in range(len(G)):
                if neighbor not in path and (neighbor, node) in G[(node, neighbor)]:
                    stack.append((neighbor, path + [neighbor]))
    
    def gaussian_elimination(A):
        n = len(A)
        m = len(A[0])
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(m):
                A[i][j] /= A[i][i]
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(m):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            for j in range(i+1, n):
                if A[i][i] == 0:
                    det = 0
                    break
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
            det *= A[i][i]
        return det
    
    def build_graph(circuit):
        n = len(circuit)
        G = [[0]*n for _ in range(n)]
        for i in range(n-1):
            if circuit[i] == 'NOT':
                G[n-1][i] = 1
            elif circuit[i] == 'AND':
                G[n-2][i] = 1
                G[n-3][i] = 1
            else:  # OR
                G[n-4][i] = 1
                G[n-5][i] = 1
        return G
    
    def count_saw_walks(G, L):
        n = len(G)
        c_L = 0
        for i in range(n):
            c_L += sum(1 for _ in count_self_avoiding_walks(G, i, L))
        return c_L
    
    def log2(x):
        if x <= 0:
            return -math.inf
        return math.log2(x)
    
    n_values = [8, 10, 12, 14, 16]
    s_values = [12, 16, 20, 24, 28, 32, 36, 40]
    instances_tested = 0
    rho_values = []
    
    for n in n_values:
        for s in s_values:
            circuit = generate_acc02_circuit(n, s)
            if circuit is None:
                continue
            N = 2048
            bias_count = 0
            for _ in range(N):
                output = simulate_circuit(circuit, n)
                if is_mod_3(output):
                    bias_count += 1
            bias = bias_count / N
            if abs(bias - 1/3) < 1/9:
                continue
            
            G = build_graph(circuit)
            L = math.floor(2 * log2(s + 2))
            if L > 14:
                L = 14
            c_L = count_saw_walks(G, L)
            rho = (log2(c_L + 1) / L) - 1
            
            instances_tested += 1
            rho_values.append(rho)
    
    if not rho_values:
        return {
            "metric_name": "rho",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    mean_rho = sum(rho_values) / len(rho_values)
    std_rho = math.sqrt(sum((x - mean_rho)**2 for x in rho_values) / len(rho_values))
    correlation = 0  # Spearman correlation not implemented
    
    return {
        "metric_name": "rho",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": all(rho >= (1/8) * log2(s) - 1 for s in s_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < (1/8)*log2(s)-1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")