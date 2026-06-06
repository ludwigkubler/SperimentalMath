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
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def circuit_representation(graph):
        n = len(graph)
        circuit = []
        for i in range(n):
            for j in graph[i]:
                if i < j:
                    circuit.append((i, j))
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit)
        dp = [0] * (n + 1)
        for i in range(n):
            dp[i + 1] = max(dp[j] for j in range(i) if circuit[j][1] < circuit[i][1]) + 1
        return max(dp)
    
    def hodge_decomposition_rank(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                A[i][j] = 1
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                for j in range(n):
                    if A[j][i] != 0:
                        for k in range(n):
                            A[k][j] -= A[k][i] * A[i][j]
                        rank += 1
        return rank
    
    n = random.randint(5, 40)
    d = random.randint(2, n - 1)
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "h(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    circuit = circuit_representation(graph)
    w_m = monotone_width(circuit)
    h_G = hodge_decomposition_rank(graph)
    
    return {
        "metric_name": "h(G)",
        "metric_value": h_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_G >= 2 * w_m,
        "counterexample": "" if h_G >= 2 * w_m else f"h(G) = {h_G}, w_m(G) = {w_m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")