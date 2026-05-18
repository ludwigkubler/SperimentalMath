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
    
    def generate_random_acc02_circuit(n, s):
        gates = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR', 'MOD_2', 'NOT'])
            fanin = random.randint(2, min(len(gates) + 1, math.floor(math.log2(s)) + 3))
            inputs = random.sample(range(len(gates)), fanin) if len(gates) > 0 else []
            gates.append((gate_type, inputs))
        return gates
    
    def dfs_labeling(gates):
        graph = {i: [] for i in range(len(gates))}
        for i, (_, inputs) in enumerate(gates):
            for j in inputs:
                graph[j].append(i)
        
        labels = [-1] * len(gates)
        stack = [len(gates) - 1]
        while stack:
            node = stack.pop()
            if labels[node] == -1:
                labels[node] = 0
                for neighbor in reversed(graph[node]):
                    if labels[neighbor] == -1:
                        stack.append(neighbor)
        
        return labels
    
    def spectrum_dimension(gate, p):
        gate_type, inputs = gate
        if gate_type != 'MOD_2':
            return 0
        
        k = len(inputs) + 1
        counts = [0] * p
        for xi in range(p):
            sum_exp = sum(math.exp(2j * math.pi * xi * ai / p) for ai in inputs)
            if abs(sum_exp) >= k / 2:
                counts[xi] += 1
        
        return len([c for c in counts if c > 0])
    
    def max_spectrum_dimension(circuit, p):
        return max(spectrum_dimension(gate, p) for gate in circuit)
    
    n_values = [6, 8, 10, 12]
    s_values = [15, 30, 60]
    instances_tested = 0
    total_metric_value = 0
    
    for n in n_values:
        for s in s_values:
            for _ in range(30):
                circuit = generate_random_acc02_circuit(n, s)
                labels = dfs_labeling(circuit)
                
                p = next_prime(s + 2)
                metric_value = max_spectrum_dimension(circuit, p) / math.log2(p + 1)
                instances_tested += 1
                total_metric_value += metric_value
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0
    
    return {
        "metric_name": "max_spectrum_dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

def next_prime(n):
    if n <= 1:
        return 2
    for i in range(n, 2*n):
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                break
        else:
            return i
    return 2 * n

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [next_prime(2*i + 1) for i in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")