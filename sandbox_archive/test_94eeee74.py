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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def term_overlap_graph(circuit):
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                overlap = set(circuit[i][1]) & set(circuit[j][1])
                if overlap:
                    G[i][j] = G[j][i] = len(overlap)
        return G
    
    def min_order(G):
        n = len(G)
        for k in range(n):
            for i in range(n):
                for j in range(i + 1, n):
                    if G[i][j] == 0:
                        continue
                    if all(G[i][k] + G[k][j] >= G[i][j] for k in range(n)):
                        return k + 1
        return n
    
    def monotone_width(circuit):
        n = len(circuit)
        max_width = 0
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            width = 0
            for gate_type, inputs in circuit:
                if all(assignment[j] for j in inputs):
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            G = term_overlap_graph(circuit)
            eta = min_order(G)
            w_m = monotone_width(circuit)
            metric_values.append((eta, w_m))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "eta_vs_w_m",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    eta_values = [eta for eta, _ in metric_values]
    w_m_values = [w_m for _, w_m in metric_values]
    
    mean_eta = sum(eta_values) / len(eta_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    correlation = 0
    if len(eta_values) > 1:
        numerator = sum((eta - mean_eta) * (w_m - mean_w_m) for eta, w_m in metric_values)
        denominator = math.sqrt(sum((eta - mean_eta)**2 for eta in eta_values)) * math.sqrt(sum((w_m - mean_w_m)**2 for w_m in w_m_values))
        correlation = numerator / denominator
    
    return {
        "metric_name": "eta_vs_w_m",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")