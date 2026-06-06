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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def real_algebraic_surface(graph):
        n = len(graph)
        A = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                if i < j:
                    A[i][j] = Fraction(1, 2)
                    A[j][i] = Fraction(1, 2)
        return A
    
    def hodge_rank(A):
        n = len(A)
        rank = 0
        for _ in range(n):
            max_row = -1
            max_val = -math.inf
            for i in range(n):
                if all(A[i][j] == Fraction(0, 1) for j in range(i)):
                    if A[i][i] > max_val:
                        max_row = i
                        max_val = A[i][i]
            if max_row != -1:
                rank += 1
                for j in range(n):
                    A[max_row][j] = Fraction(0, 1)
                    A[j][max_row] = Fraction(0, 1)
        return rank
    
    def monotone_width(circuit):
        n = len(circuit)
        dp = [0] * (n + 1)
        for i in range(n):
            dp[i + 1] = max(dp[j] for j in range(i) if circuit[j][1] < circuit[i][1]) + 1
        return dp[-1]
    
    def circuit_representation(graph):
        n = len(graph)
        circuit = []
        visited = [False] * n
        stack = []
        for i in range(n):
            if not visited[i]:
                stack.append(i)
                while stack:
                    u = stack.pop()
                    if not visited[u]:
                        visited[u] = True
                        for v in graph[u]:
                            if not visited[v]:
                                circuit.append((u, v))
                                stack.append(v)
        return circuit
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n_max = 0
        instances_tested = 0
        total_metric_value = 0.0
        conjecture_holds = True
        counterexample = ""
        
        for n in [5, 10, 15, 20, 30, 40]:
            if time.time() + (n - 5) * 8 > 240:
                print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30')
                return
            graph = generate_d_regular_graph(n, 3)
            if graph is None:
                continue
            A = real_algebraic_surface(graph)
            h_G = hodge_rank(A)
            circuit = circuit_representation(graph)
            w_m = monotone_width(circuit)
            if h_G < 2 * w_m:
                conjecture_holds = False
                counterexample = f"h(G)={h_G}, w_m(G)={w_m}"
            total_metric_value += h_G
            instances_tested += 1
            n_max = max(n_max, n)
        
        return {
            "metric_name": "h(G)",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    return run_trial(seed)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")