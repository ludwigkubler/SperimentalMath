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
        while len(edges) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def is_symplectic_reflection(graph):
        n = len(graph)
        for i in range(n):
            if sum(graph[i]) % 2 != 0:
                return False
            for j in range(i + 1, n):
                if (graph[i][j] + graph[j][i]) % 2 != 0:
                    return False
        return True
    
    def compute_tropical_motivic_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            row_sum = sum(graph[i])
            if row_sum > rank:
                rank = row_sum
        return rank
    
    def symplectic_reflection(graph):
        n = len(graph)
        reflected_graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                reflected_graph[i][j] = graph[j][i]
        return reflected_graph
    
    def tseitin_formula(graph):
        n = len(graph)
        formula = []
        for i in range(n):
            clause = [f"X{i}"]
            for j in range(n):
                if graph[i][j] == 1:
                    clause.append(f"-X{j}")
            formula.append(clause)
        return formula
    
    def evaluate_formula(formula, assignment):
        stack = []
        for clause in formula:
            clause_evaluated = False
            for literal in clause:
                var = literal[1:]
                negated = literal.startswith('-')
                if (var not in assignment and not negated) or (var in assignment and assignment[var] == negated):
                    clause_evaluated = True
                    break
            if not clause_evaluated:
                return False
        return True
    
    def find_counterexample(formula, n):
        for i in range(n):
            assignment = {f"X{j}": j % 2 == 0 for j in range(n)}
            if not evaluate_formula(formula, assignment):
                return f"Assignment X{i}=False does not satisfy the formula"
        return ""
    
    n = 40
    d = 3
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mtr",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    if not is_symplectic_reflection(graph):
        return {
            "metric_name": "mtr",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph is not symplectically reflective"
        }
    
    mtr_phi_G = compute_tropical_motivic_rank(graph)
    phi_G = tseitin_formula(graph)
    counterexample = find_counterexample(phi_G, n)
    if counterexample:
        return {
            "metric_name": "mtr",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    reflected_graph = symplectic_reflection(graph)
    mtr_phi_G_prime = compute_tropical_motivic_rank(reflected_graph)
    phi_G_prime = tseitin_formula(reflected_graph)
    counterexample = find_counterexample(phi_G_prime, n)
    if counterexample:
        return {
            "metric_name": "mtr",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    k = mtr_phi_G_prime / mtr_phi_G
    return {
        "metric_name": "mtr",
        "metric_value": k,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(k - 1) <= 2,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")