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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def term_overlap_graph(circuit):
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(input_i == input_j for input_i, input_j in zip(circuit[i][1], circuit[j][1])):
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def min_order(G):
        n = len(G)
        visited = [False] * n
        order = []
        
        def dfs(v):
            stack = [v]
            while stack:
                v = stack.pop()
                if not visited[v]:
                    visited[v] = True
                    for i in range(n):
                        if G[v][i] and not visited[i]:
                            stack.append(i)
                    order.append(v)
        
        for v in range(n):
            if not visited[v]:
                dfs(v)
        
        return len(order) == n
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(2**n):
            active_gates = [j for j, (_, inputs) in enumerate(circuit) if all(inputs[k] & i for k in range(len(inputs)))]
            width = max(width, len(active_gates))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        G = term_overlap_graph(circuit)
        eta_value = min_order(G)
        w_m_value = monotone_width(circuit)
        results.append((eta_value, w_m_value))
    
    if len(results) < 30:
        return {
            "metric_name": "eta_wm_correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    eta_values = [res[0] for res in results]
    w_m_values = [res[1] for res in results]
    
    mean_eta = sum(eta_values) / len(eta_values)
    mean_wm = sum(w_m_values) / len(w_m_values)
    std_eta = math.sqrt(sum((x - mean_eta)**2 for x in eta_values) / len(eta_values))
    std_wm = math.sqrt(sum((x - mean_wm)**2 for x in w_m_values) / len(w_m_values))
    
    correlation_coefficient = sum((eta_values[i] - mean_eta) * (w_m_values[i] - mean_wm) for i in range(len(eta_values))) / (len(eta_values) * std_eta * std_wm)
    
    return {
        "metric_name": "eta_wm_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")