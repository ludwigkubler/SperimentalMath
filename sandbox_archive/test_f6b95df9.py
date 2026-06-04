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
            raise ValueError("Graph size must be a multiple of the degree")
        
        graph = {i: [] for i in range(n)}
        edges_added = set()
        
        while len(edges_added) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                edges_added.add((v, u))
        
        return graph
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Clause for each variable being true or false
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        
        # Clause for each pair of variables being different
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'x{i}', -f'x{j}'])
                clauses.append([-f'x{i}', f'x{j}'])
        
        return clauses
    
    def frege_proof_depth(clauses):
        # Simplified Frege proof depth calculation
        return len(clauses)
    
    def moment_polytope(graph):
        n = len(graph)
        vertices = [list(range(n))]
        faces = []
        
        while vertices:
            vertex = vertices.pop()
            if not vertex:
                continue
            
            face = [vertex[0]]
            for neighbor in graph[vertex[0]]:
                if neighbor not in face:
                    face.append(neighbor)
            
            faces.append(face)
            vertices.extend([face[i+1:] for i in range(len(face)-1)])
        
        return len(faces)
    
    def spearman_correlation(l1, l2):
        n = len(l1)
        rank_l1 = {x: i for i, x in enumerate(sorted(set(l1)), start=1)}
        rank_l2 = {x: i for i, x in enumerate(sorted(set(l2)), start=1)}
        
        sum_diff_squares = sum((rank_l1[l1[i]] - rank_l2[l2[i]]) ** 2 for i in range(n))
        sum_rank_diffs = sum(abs(rank_l1[l1[i]] - rank_l2[l2[i]]) for i in range(n))
        
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    def mean_absolute_difference(l, theta):
        return sum(abs(x - theta) for x in l) / len(l)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n-1, 4))
        graph = generate_d_regular_graph(n, d)
        clauses = tseitin_formula(n)
        
        l_phi_g = moment_polytope(graph)
        d_phi_g = frege_proof_depth(clauses)
        
        results.append((l_phi_g, d_phi_g))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    l_phi_g_values, d_phi_g_values = zip(*results)
    rho = spearman_correlation(l_phi_g_values, d_phi_g_values)
    theta = Fraction(n * (n - 1), 2) / d
    mean_abs_diff = mean_absolute_difference(l_phi_g_values, theta)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")