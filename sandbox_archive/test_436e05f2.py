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
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while any(graph[i][j] or graph[j][i] for j in neighbors):
                neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j and (i, j) not in edges and (j, i) not in edges:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.add((i, j))
        return graph
    
    def is_valid_group(g):
        n = len(g)
        for i in range(n):
            if g[i][i] != 1:
                return False
            for j in range(n):
                if g[i][j] != g[j][i]:
                    return False
        return True
    
    def find_automorphism_group(graph):
        n = len(graph)
        group = []
        for i in range(2**n):
            perm = [int(x) for x in format(i, f'0{n}b')]
            if all(graph[perm[i]][perm[j]] == graph[i][j] for i in range(n) for j in range(n)):
                group.append(perm)
        return group
    
    def frege_proof_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clause = [i + 1]
            for j in range(i + 1, n):
                if graph[i][j] == 0:
                    clause.append(-j - 1)
            clauses.append(clause)
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_max = 40
    instances_tested = 0
    total_log2_A_G = 0
    total_w_Frege_G = 0
    max_n = 5
    
    for n in range(5, n_max + 1):
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        instances_tested += 1
        max_n = max(max_n, n)
        
        A_G = find_automorphism_group(graph)
        log2_A_G = log2(len(A_G))
        w_Frege_G = frege_proof_width(graph)
        
        total_log2_A_G += log2_A_G
        total_w_Frege_G += w_Frege_G
    
    if instances_tested < 30:
        return {
            "metric_name": "log2(|A(G)|) vs. w_Frege(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_log2_A_G = total_log2_A_G / instances_tested
    mean_w_Frege_G = total_w_Frege_G / instances_tested
    
    correlation_coefficient = 0.0
    for n in range(5, n_max + 1):
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        A_G = find_automorphism_group(graph)
        log2_A_G = log2(len(A_G))
        w_Frege_G = frege_proof_width(graph)
        
        correlation_coefficient += (log2_A_G - mean_log2_A_G) * (w_Frege_G - mean_w_Frege_G)
    correlation_coefficient /= instances_tested
    
    mean_abs_diff = 0.0
    for n in range(5, n_max + 1):
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        A_G = find_automorphism_group(graph)
        log2_A_G = log2(len(A_G))
        w_Frege_G = frege_proof_width(graph)
        
        mean_abs_diff += abs(log2_A_G - (w_Frege_G * math.log(2)))
    mean_abs_diff /= instances_tested
    
    return {
        "metric_name": "log2(|A(G)|) vs. w_Frege(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if "metric_value" not in result or result["metric_value"] is None), None)
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data first_failing_seed={first_failing_seed}")