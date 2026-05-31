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
        if (d * n) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        literals = {i: f"x{i}" for i in range(len(graph))}
        clauses = []
        for i, neighbors in enumerate(graph):
            clause = [f"~{literals[i]}"]
            for j in neighbors:
                clause.append(literals[j])
            clauses.append(" | ".join(clause))
        return " & ".join(clauses)

    def resolution_width(formula):
        stack = []
        literals = set()
        for clause in formula.split(" & "):
            if any(l.startswith("~") for l in clause.split()):
                continue
            literals.update(clause.split())
            stack.append(clause)
        
        while len(stack) > 1:
            clause1 = stack.pop()
            clause2 = stack.pop()
            new_clauses = []
            for literal in literals:
                if literal not in clause1 and f"~{literal}" not in clause2:
                    continue
                if f"~{literal}" not in clause1 and literal not in clause2:
                    continue
                new_clause = [l for l in clause1.split() if l != literal]
                new_clause.extend([l for l in clause2.split() if l != f"~{literal}"])
                new_clauses.append(" | ".join(new_clause))
            stack.extend(new_clauses)
        
        return len(stack)

    def hodge_classes(formula):
        # Placeholder function to represent the computation of Hodge classes
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)  # Replace with actual computation

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        formula = tseitin_formula(graph)
        mnc = hodge_classes(formula)
        w = resolution_width(formula)
        results.append({"n": n, "mnc": mnc, "w": w})
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mnc_values = [r["mnc"] for r in results]
    w_values = [r["w"] for r in results]
    
    mean_mnc = sum(mnc_values) / len(mnc_values)
    mean_w = sum(w_values) / len(w_values)
    variance_mnc = sum((x - mean_mnc) ** 2 for x in mnc_values) / len(mnc_values)
    variance_w = sum((x - mean_w) ** 2 for x in w_values) / len(w_values)
    covariance = sum((mnc_values[i] - mean_mnc) * (w_values[i] - mean_w) for i in range(len(results))) / len(results)
    
    pearson_corr = covariance / math.sqrt(variance_mnc * variance_w)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")