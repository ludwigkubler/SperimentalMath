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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def is_valid_circuit(circuit):
        stack = []
        for op in circuit:
            if op == 'PUSH':
                stack.append(0)
            elif op == 'ADD':
                if len(stack) < 2:
                    return False
                stack[-2] += stack.pop()
            elif op == 'MUL':
                if len(stack) < 2:
                    return False
                stack[-2] *= stack.pop()
            else:
                return False
        return len(stack) == 1 and stack[0] == 0
    
    def circuit_width(circuit):
        max_depth = 0
        current_depth = 0
        for op in circuit:
            if op == 'PUSH':
                current_depth += 1
            elif op == 'ADD' or op == 'MUL':
                current_depth -= 1
            max_depth = max(max_depth, current_depth)
        return max_depth
    
    def hodge_decomposition_rank(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        for u in graph:
            for v in graph[u]:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
        
        def gaussian_elimination(matrix, n):
            rank = 0
            for i in range(n):
                if matrix[i][i] == 0:
                    swap_found = False
                    for j in range(i + 1, n):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            swap_found = True
                            break
                    if not swap_found:
                        continue
                pivot = matrix[i][i]
                for j in range(n):
                    matrix[i][j] /= pivot
                for k in range(n):
                    if k != i and matrix[k][i] != 0:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
                rank += 1
            return rank
        
        return gaussian_elimination(adj_matrix, n)
    
    def circuit_representation(graph):
        n = len(graph)
        circuit = []
        for u in graph:
            for v in graph[u]:
                if u < v:
                    circuit.append('PUSH')
                    circuit.append('PUSH')
                    circuit.append('MUL')
                    circuit.append('ADD')
        return circuit
    
    def monotone_width(circuit):
        return circuit_width(circuit)
    
    n = 10
    d = 3
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "h(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    circuit = circuit_representation(graph)
    if not is_valid_circuit(circuit):
        return {
            "metric_name": "h(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid circuit"
        }
    
    h_G = hodge_decomposition_rank(graph)
    w_m_G = monotone_width(circuit)
    
    return {
        "metric_name": "h(G)",
        "metric_value": h_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_G >= 2 * w_m_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")