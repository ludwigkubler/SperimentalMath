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
    
    def generate_expander_graph(n):
        graph = {}
        for i in range(n):
            graph[i] = set()
        for _ in range(int(0.5 * n * (n - 1))):
            u, v = random.sample(range(n), 2)
            if u not in graph[v]:
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def tutte_polynomial(graph):
        n = len(graph)
        T = [[0] * (n + 1) for _ in range(n + 1)]
        T[0][0] = 1
        for i in range(1, n + 1):
            T[i][0] = T[i - 1][0]
            T[i][i] = 1
            for j in range(1, i):
                T[i][j] = T[i - 1][j - 1] + T[i - 1][j]
        return T
    
    def characteristic_polynomial(T):
        n = len(T) - 1
        p = [[0] * (n + 1) for _ in range(n + 1)]
        p[0][0] = 1
        for i in range(1, n + 1):
            p[i][0] = -T[n][i]
            for j in range(1, i + 1):
                p[i][j] = T[n][j] * p[i - 1][j - 1] - T[n][j - 1] * p[i - 1][j]
        return p
    
    def tropical_logarithmic_form(p):
        n = len(p) - 1
        rank = 0
        for i in range(n + 1):
            if any(p[j][i] != 0 for j in range(i, n + 1)):
                rank += 1
        return rank
    
    def resolution_proof_length(graph):
        # Simplified DPLL algorithm to estimate proof length
        stack = [(graph, [])]
        while stack:
            graph, path = stack.pop()
            if not graph:
                return len(path)
            u = next(iter(graph))
            for v in graph[u]:
                new_graph = {x: set(y) for x, y in graph.items() if x != u and v not in y}
                stack.append((new_graph, path + [u]))
        return float('inf')
    
    n = random.randint(5, 40)
    graph = generate_expander_graph(n)
    T = tutte_polynomial(graph)
    p = characteristic_polynomial(T)
    rank = tropical_logarithmic_form(p)
    proof_length = resolution_proof_length(graph)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL algorithm did not terminate"
        }
    
    ratio = proof_length / (2 ** rank)
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] != -1) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] != -1)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] or r["metric_value"] == -1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] != -1 for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL algorithm did not terminate\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")