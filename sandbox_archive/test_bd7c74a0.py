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
    
    def generate_planar_graph(n):
        if n < 3 or n > 40:
            return None
        nodes = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0 and len(edges) < 2 * (n - 1):
                    edges.append((i, j))
        return nodes, edges
    
    def is_planar(graph):
        nodes, edges = graph
        if len(nodes) <= 4:
            return True
        for node in nodes:
            neighbors = [e[1] if e[0] == node else e[0] for e in edges if e[0] == node or e[1] == node]
            subgraph = (nodes, [(u, v) for u, v in edges if u not in neighbors and v not in neighbors])
            if not is_planar(subgraph):
                return False
        return True
    
    def term_overlap_graph(graph):
        nodes, edges = graph
        n = len(nodes)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in edges or (j, i) in edges:
                    T[i][j] = 1
                    T[j][i] = 1
        return T
    
    def minimal_rank(T):
        n = len(T)
        rank = 0
        for row in T:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            T[j][i] -= T[j][j]
        return rank
    
    def communication_complexity_growth_rate(graph, n):
        # Placeholder function to simulate growth rate calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.uniform(0.1, 2.0)
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_planar_graph(n)
        if not is_planar(graph):
            continue
        
        T = term_overlap_graph(graph)
        r_TG = minimal_rank(T)
        growth_rate_G = communication_complexity_growth_rate(graph, n)
        
        if 'communication_rank' not in locals():
            communication_rank = []
        
        communication_rank.append((r_TG, growth_rate_G))
    
    if len(communication_rank) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(communication_rank),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n_val for _, n_val in communication_rank)),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    r_values = [x[0] for x in communication_rank]
    growth_rate_values = [x[1] for x in communication_rank]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation(r_values, growth_rate_values)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(communication_rank),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == n_val for _, n_val in communication_rank)),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")