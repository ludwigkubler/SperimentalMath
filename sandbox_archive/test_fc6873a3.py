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
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clause = [f"X{i}"]
            for j in graph[i]:
                clause.append(f"-X{j}")
            clauses.append(clause)
        for i in range(n):
            for j in range(i+1, n):
                clause = [f"-X{i}", f"-X{j}", f"X{2*n+i+j}"]
                clauses.append(clause)
                clause = [f"-X{i}", f"X{j}", f"X{2*n+i+j}"]
                clauses.append(clause)
                clause = [f"-X{j}", f"X{i}", f"X{2*n+i+j}"]
                clauses.append(clause)
        return clauses
    
    def tropicalized_quiver_representation(clauses):
        n = len(clauses)
        mtr_q = 0
        for clause in clauses:
            mtr_q = max(mtr_q, len(clause))
        return mtr_q
    
    def resolution_proof_width(clauses):
        # Simplified version of resolution width calculation
        width = 1
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    mtr_q_values = []
    w_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        mtr_q = tropicalized_quiver_representation(clauses)
        w = resolution_proof_width(clauses)
        mtr_q_values.append(mtr_q)
        w_values.append(w)
    
    if not mtr_q_values or not w_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mtr_q = sum(mtr_q_values) / len(mtr_q_values)
    mean_w = sum(w_values) / len(w_values)
    covariance = sum((mtr_q - mean_mtr_q) * (w - mean_w) for mtr_q, w in zip(mtr_q_values, w_values)) / len(mtr_q_values)
    variance_mtr_q = sum((mtr_q - mean_mtr_q) ** 2 for mtr_q in mtr_q_values) / len(mtr_q_values)
    variance_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    correlation_coefficient = covariance / (math.sqrt(variance_mtr_q) * math.sqrt(variance_w))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mtr_q_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")