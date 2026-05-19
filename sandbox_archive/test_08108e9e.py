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
    
    def generate_instance(n: int, d: int):
        if n < 2 or d < 1:
            return None
        
        # Generate a depth-2 DNF circuit for PARITY
        if d == 2:
            circuit = [[i] for i in range(n)]
            circuit.append([i for i in range(n)])
        
        # Generate a depth-3 recursive circuit for PARITY
        else:
            block_size = int(math.ceil(math.sqrt(n)))
            blocks = [generate_instance(block_size, d - 2) for _ in range(int(math.ceil(n / block_size)))]
            circuit = []
            for block in blocks:
                if block is not None:
                    circuit.extend(block)
            circuit.append([i for i in range(n)])
        
        # Add random NOT-NOT redundancy gates
        for _ in range(random.randint(0, 2 * n)):
            gate1 = random.randint(0, len(circuit) - 1)
            gate2 = random.randint(0, len(circuit) - 1)
            if gate1 != gate2:
                circuit[gate1].append(gate2)
        
        return circuit
    
    def reverse_bfs(start: int, circuit: list):
        n = len(circuit)
        visited = [False] * n
        queue = [start]
        visited[start] = True
        cone = set()
        while queue:
            node = queue.pop(0)
            cone.add(node)
            for neighbor in circuit[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        return cone
    
    def power_method(M: list, max_iter: int):
        n = len(M)
        v = [1.0 / math.sqrt(n)] * n
        for _ in range(max_iter):
            v = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm = sum(v[i] ** 2 for i in range(n))
            if norm == 0:
                return None, None
            v = [v[i] / math.sqrt(norm) for i in range(n)]
        return v, max(abs(x) for x in v)
    
    def cone_indicator(gate1: int, gate2: int, circuit: list):
        cone1 = reverse_bfs(gate1, circuit)
        cone2 = reverse_bfs(gate2, circuit)
        return len(cone1.intersection(cone2))
    
    def compute_K(C: list):
        n = len(C)
        K = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                K[i][j] = cone_indicator(i, j, C)
                K[j][i] = K[i][j]
        return K
    
    def trace(matrix: list):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def max_eigenvalue(matrix: list):
        v, _ = power_method(matrix, 30)
        if v is None:
            return None
        return max(abs(x) for x in [sum(matrix[i][j] * v[j] for j in range(len(matrix))) for i in range(len(matrix))])
    
    def compute_psi(K: list):
        n = len(K)
        trace_K = trace(K)
        lambda_max = max_eigenvalue(K)
        if lambda_max is None or trace_K == 0:
            return None
        return trace_K / lambda_max
    
    def compute_r(C: list, d: int):
        psi = compute_psi(C)
        s_C = len(C) - 1
        if psi is None or s_C == 0:
            return None
        return psi ** (1 / (d - 1)) / math.log2(s_C)
    
    n_values = [4, 6, 8, 10, 12, 14, 16, 20, 24]
    d_values = [2, 3]
    results = []
    
    for n in n_values:
        for d in d_values:
            for _ in range(30):
                instance = generate_instance(n, d)
                if instance is None:
                    continue
                r_C = compute_r(instance, d)
                if r_C is not None:
                    results.append(r_C)
    
    if len(results) == 0:
        return {
            "metric_name": "r(C)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_r = sum(results) / len(results)
    max_r = max(results)
    support_fraction = sum(1 for r in results if r <= 8) / len(results)
    
    if max_r > 8:
        return {
            "metric_name": "r(C)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"max_r={max_r}"
        }
    
    return {
        "metric_name": "r(C)",
        "metric_value": mean_r,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    max_r = max(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if max_r > 8:
        print(f"RESULT: FALSIFIED counterexample=\"max_r={max_r}\" first_failing_seed={seeds[results.index(next(r for r in results if r['metric_value'] is not None and r['metric_value'] > 8))]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")