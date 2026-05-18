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
    
    def build_gate_graph(d, s):
        gates = ['AND', 'OR', 'NOT', 'MOD_2']
        graph = [[] for _ in range(s)]
        for i in range(1, s):
            for j in range(i):
                gate_type = random.choice(gates)
                if gate_type == 'MOD_2':
                    continue
                graph[i].append(j)
                graph[j].append(i)
        return graph
    
    def bfs(graph, start):
        n = len(graph)
        distances = [float('inf')] * n
        distances[start] = 0
        queue = [start]
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return distances
    
    def compute_delta(graph):
        n = len(graph)
        max_distance = float('-inf')
        for i in range(n):
            dist_i = bfs(graph, i)
            for j in range(i+1, n):
                dist_j = bfs(graph, j)
                for k in range(j+1, n):
                    dist_k = bfs(graph, k)
                    for l in range(k+1, n):
                        d_ik = dist_i[k]
                        d_ij = dist_i[j]
                        d_jk = dist_j[k]
                        d_jl = dist_j[l]
                        d_ikj = max(d_ij + d_jk, d_ik + d_kj)
                        d_ilj = max(d_ij + d_lj, d_il + d_jl)
                        distance = (d_ik + d_jl - d_ikj) / 2
                        if distance > max_distance:
                            max_distance = distance
        return max_distance
    
    def compute_mod_3_bias(circuit):
        n = len(circuit)
        count = 0
        for x in range(1 << n):
            result = circuit[x]
            mod_3_result = sum(int(bit) for bit in bin(x)[2:]) % 3
            if result == mod_3_result:
                count += 1
        return 2 * (count / (1 << n)) - 1
    
    def build_circuit(d, s):
        circuit = [random.randint(0, 1) for _ in range(1 << s)]
        return circuit
    
    d_values = [2, 3, 4]
    s_values = [12, 18, 24]
    n_values = [8, 10, 12]
    
    max_ratio = 0
    for d in d_values:
        for s in s_values:
            for n in n_values:
                graph = build_gate_graph(d, s)
                delta = compute_delta(graph)
                circuit = build_circuit(d, s)
                bias = compute_mod_3_bias(circuit)
                lhs = abs(bias) ** 2 * n
                rhs = (1 + delta) * 2 ** d
                ratio = lhs / rhs
                if ratio > max_ratio:
                    max_ratio = ratio
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": len(d_values) * len(s_values) * len(n_values),
        "conjecture_holds": max_ratio <= 1.0,
        "counterexample": "" if max_ratio <= 1.0 else f"max_ratio={max_ratio} > 1.0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std=0.0000 support_fraction=1.0000")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")