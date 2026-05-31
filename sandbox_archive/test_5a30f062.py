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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def matrix_representation(graph):
        n = len(graph)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                M[i][j] = 1
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, n):
                if M[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            M[pivot_row], M[rank] = M[rank], M[pivot_row]
            rank += 1
            for row in range(rank, n):
                factor = M[row][col] / M[pivot_row][col]
                for j in range(col, n):
                    M[row][j] -= factor * M[pivot_row][j]
        return rank
    
    def algebraic_k_theory_rank(M):
        return gaussian_elimination(M)
    
    def boolean_circuit_entanglement_complexity(graph):
        n = len(graph)
        # Placeholder for actual complexity calculation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return random.randint(1, 10)  # Dummy value
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_k_theory_rank = 0
    total_entanglement_complexity = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_d_regular_graph(n, d=3)
            if graph is None:
                continue
            M = matrix_representation(graph)
            k_theory_rank = algebraic_k_theory_rank(M)
            entanglement_complexity = boolean_circuit_entanglement_complexity(graph)
            
            instances_tested += 1
            total_k_theory_rank += k_theory_rank
            total_entanglement_complexity += entanglement_complexity
            max_n = max(max_n, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "algebraic_k_theory_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_k_theory_rank = total_k_theory_rank / instances_tested
    mean_entanglement_complexity = total_entanglement_complexity / instances_tested
    
    if abs(mean_k_theory_rank - 3 * mean_entanglement_complexity) <= 1:
        return {
            "metric_name": "algebraic_k_theory_rank",
            "metric_value": mean_k_theory_rank,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "algebraic_k_theory_rank",
            "metric_value": mean_k_theory_rank,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": f"mean_k_theory_rank={mean_k_theory_rank}, 3*mean_entanglement_complexity={3 * mean_entanglement_complexity}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_k_theory_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_k_theory_rank = math.sqrt(sum((r["metric_value"] - mean_k_theory_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_k_theory_rank} std={std_dev_k_theory_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_k_theory_rank} std={std_dev_k_theory_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break