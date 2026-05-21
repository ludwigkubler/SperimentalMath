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
    
    def generate_3regular_graph(m):
        while True:
            vertices = list(range(m))
            edges = set()
            degrees = [0] * m
            for _ in range(m):
                u, v = random.sample(vertices, 2)
                if (u, v) not in edges and (v, u) not in edges and degrees[u] < 3 and degrees[v] < 3:
                    edges.add((u, v))
                    degrees[u] += 1
                    degrees[v] += 1
            if all(d == 3 for d in degrees):
                return edges
    
    def compute_edge_expansion(edges, m):
        min_cut = float('inf')
        for i in range(1, m // 2 + 1):
            for subset in itertools.combinations(range(m), i):
                cut_size = sum(1 for u, v in edges if (u in subset and v not in subset) or (v in subset and u not in subset))
                min_cut = min(min_cut, cut_size / i)
        return min_cut
    
    def generate_odd_charging(m):
        sigma = {}
        for v in range(m):
            sigma[v] = random.choice([0, 1])
        if sum(sigma.values()) % 2 == 0:
            sigma[random.randint(0, m - 1)] = 1 - sigma[random.randint(0, m - 1)]
        return sigma
    
    def tseitin(v):
        if v < m:
            return sigma[v]
        else:
            u, w = edges[v - m]
            return (tseitin(u), tseitin(w))
    
    def build_truth_table():
        truth_table = []
        for i in range(2 ** m):
            assignment = [(i >> j) & 1 for j in range(m)]
            truth_table.append(tseitin(sum(assignment)))
        return truth_table
    
    def matrix_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for r in range(rows):
                if r != pivot_row:
                    factor = matrix[r][col] / matrix[pivot_row][col]
                    for c in range(cols):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
        return rank
    
    m_values = [4, 6, 8, 10, 12, 14]
    results = []
    
    for m in m_values:
        edges = generate_3regular_graph(m)
        sigma = generate_odd_charging(m)
        h_G = compute_edge_expansion(edges, m)
        
        truth_table = build_truth_table()
        rank = matrix_rank(truth_table)
        
        log2_rank = math.log2(rank) if rank > 0 else -math.inf
        results.append({
            "m": m,
            "h(G)": h_G,
            "log2_rank": log2_rank,
            "expected_value": 0.25 * h_G * m
        })
    
    support_check = all(result["log2_rank"] >= result["expected_value"] for result in results)
    if not support_check:
        return {
            "metric_name": "log2_rank",
            "metric_value": sum(result["log2_rank"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "support_check_failed"
        }
    
    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress([result["h(G)"] * result["m"] for result in results], [result["log2_rank"] for result in results])
    
    if slope < 0.25 or p_value >= 0.01:
        return {
            "metric_name": "log2_rank",
            "metric_value": sum(result["log2_rank"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"regression_slope={slope}, p_value={p_value}"
        }
    
    return {
        "metric_name": "log2_rank",
        "metric_value": sum(result["log2_rank"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_check_failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_check_failed")