# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import product

def generate_random_circuit(n):
    num_gates = random.randint(2, 10)
    circuit = []
    for _ in range(num_gates):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            inputs = [random.randint(0, n-1) for _ in range(random.randint(2, n))]
        else:
            inputs = [random.randint(0, n-1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    return circuit

def term_overlap_graph(circuit):
    n = len(circuit)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if set(circuit[i][1]).intersection(set(circuit[j][1])):
                G[i][j] = 1
                G[j][i] = 1
    return G

def eta_invariant(G):
    n = len(G)
    def dfs(node, visited):
        stack = [node]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if G[node][neighbor] and not visited[neighbor]:
                        stack.append(neighbor)
    
    visited = [False] * n
    dfs(0, visited)
    return Fraction(sum(visited), n)

def monotone_width(circuit):
    n = len(circuit)
    max_width = 0
    for assignment in product([0, 1], repeat=n):
        width = 0
        for gate in circuit:
            if all(assignment[i] == (gate[1][i] % 2) for i in gate[1]):
                width += 1
        max_width = max(max_width, width)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            G = term_overlap_graph(circuit)
            eta_val = eta_invariant(G)
            w_m = monotone_width(circuit)
            results.append((eta_val, w_m))
    
    if not results:
        return {
            "metric_name": "eta_invariant vs monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    eta_vals = [r[0] for r in results]
    w_ms = [r[1] for r in results]
    mean_eta = sum(eta_vals) / len(eta_vals)
    mean_w_m = sum(w_ms) / len(w_ms)
    std_eta = (sum((x - mean_eta)**2 for x in eta_vals) / len(eta_vals))**0.5
    std_w_m = (sum((x - mean_w_m)**2 for x in w_ms) / len(w_ms))**0.5
    
    correlation_coefficient = sum((eta_vals[i] - mean_eta) * (w_ms[i] - mean_w_m) for i in range(len(eta_vals))) / (len(eta_vals) * std_eta * std_w_m)
    
    return {
        "metric_name": "eta_invariant vs monotone_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")