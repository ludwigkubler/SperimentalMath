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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges or (v, u) in edges:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                break
        
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        
        for i in range(n):
            clause = [f"p{i}"]
            for j in graph[i]:
                clause.append(f"-p{j}")
            clauses.append(clause)
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) == 0 or len(graph[j]) == 0:
                    continue
                clause = [f"p{i}", f"p{j}"]
                for k in graph[i]:
                    clause.append(f"-p{k}")
                clauses.append(clause)
        
        return clauses
    
    def automorphism_group(graph):
        n = len(graph)
        vertices = list(range(n))
        aut = []
        
        def dfs(v, mapping, used):
            if v in mapping:
                return
            for u in vertices:
                if u not in used and all(graph[v][j] == graph[u][mapping[j]] for j in range(len(graph[v]))):
                    mapping[v] = u
                    used.add(u)
                    dfs(v + 1, mapping, used)
                    del mapping[v]
                    used.remove(u)
        
        dfs(0, {}, set())
        return aut
    
    def log_factorial(n):
        if n == 0:
            return Fraction(0)
        result = Fraction(0)
        for i in range(2, n + 1):
            result += math.log(i)
        return result
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 0
    instances_tested = 0
    log_A_G_values = []
    phi_G_values = []
    
    for d in [3, 4, 5, 6, 7, 8, 9, 10]:
        for _ in range(30):
            n = random.randint(5, 20)
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            phi_G = tseitin_formula(graph)
            A_G = automorphism_group(graph)
            
            if not A_G:
                continue
            
            log_A_G = len(A_G) * math.log(len(A_G))
            log_A_G_values.append(log_A_G)
            phi_G_values.append(len(phi_G))
            
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = pearson_correlation(log_A_G_values, phi_G_values)
    conjecture_holds = False
    counterexample = ""
    
    if correlation_coefficient >= 0.8:
        for log_A_G, phi_G in zip(log_A_G_values, phi_G_values):
            ratio = log_A_G / phi_G
            if ratio <= 1.5 or ratio >= 0.5:
                conjecture_holds = True
                break
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    std_C = math.sqrt(sum((result["metric_value"] - mean_C) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, result in enumerate(results) if not result['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")