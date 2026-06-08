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
    
    def generate_graph(v):
        edges = set()
        while len(edges) < v:
            u, v2 = random.sample(range(v), 2)
            if (u, v2) not in edges and (v2, u) not in edges:
                edges.add((u, v2))
        return [sorted(e) for e in edges]
    
    def is_3_regular(graph):
        degrees = [sum(1 for edge in graph if i in edge) for i in range(len(graph))]
        return all(d == 3 for d in degrees)
    
    def generate_tseitin_formula(v):
        clauses = []
        variables = list(range(v))
        for var in variables:
            clause = [-var, -var, var]
            clauses.append(clause)
        for i in range(1, v):
            clause = [variables[i-1], variables[i]]
            clauses.append(clause)
        return clauses
    
    def generate_point_cloud(clauses):
        n = len(clauses) * 3
        point_cloud = []
        for clause in clauses:
            point = [-1 if c < 0 else 1 for c in clause]
            point_cloud.extend(point)
        return point_cloud
    
    def vietoris_rips_complex(points, scale):
        # Simplified Vietoris-Rips complex construction
        n = len(points)
        simplices = []
        for i in range(n):
            simplices.append([i])
        for j in range(n):
            for k in range(j+1, n):
                dist = sum((points[i] - points[j]) ** 2 for i in range(len(points[0]))) ** 0.5
                if dist <= scale:
                    simplices.append([j, k])
        return simplices
    
    def persistent_homology(simplices):
        # Simplified persistence homology calculation
        birth = [float('inf')] * len(simplices)
        death = [-1] * len(simplices)
        for i in range(len(simplices)):
            for j in range(i+1, len(simplices)):
                if set(simplices[i]).issubset(set(simplices[j])):
                    birth[j] = min(birth[j], birth[i])
                    death[j] = max(death[j], death[i])
        return [d - b for b, d in zip(birth, death) if d != -1]
    
    def resolution_width(clauses):
        # Simplified width-bounded resolution search
        max_width = 0
        for i in range(1, len(clauses)):
            stack = [(clauses[:i], set())]
            while stack:
                current_clauses, assignment = stack.pop()
                if not current_clauses:
                    continue
                clause = current_clauses[-1]
                var = abs(clause[0])
                for val in [-1, 1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    new_clauses = [c for c in current_clauses[:-1] if not any(abs(c[j]) == var and c[j] != val * clause[j] for j in range(len(c)))]
                    stack.append((new_clauses, new_assignment))
                max_width = max(max_width, len(assignment))
        return max_width
    
    def least_squares_fit(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def log_base_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    v_values = [6, 8, 10, 12, 14, 16]
    results = []
    for v in v_values:
        graph = generate_graph(v)
        if not is_3_regular(graph):
            continue
        clauses = generate_tseitin_formula(v)
        point_cloud = generate_point_cloud(clauses)
        simplices = vietoris_rips_complex(point_cloud, 2 * math.sqrt(3))
        lifespans = persistent_homology(simplices)
        L1 = sum(lifespans)
        width = resolution_width(clauses)
        results.append({
            "metric_name": "w(L1)",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": v,
            "conjecture_holds": width <= 10 * (L1 + log_base_2(v)),
            "counterexample": "" if width <= 10 * (L1 + log_base_2(v)) else f"v={v}, w={width}, L1+log2(n)={L1+log_base_2(v)}"
        })
    
    return {
        "metric_name": "w(L1)",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results)) ** 0.5
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next((r["seed"] for r in all_results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")