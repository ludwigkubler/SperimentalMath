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
        if n * d % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    edges.add((i, j))
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def find_minimal_representation(graph):
        n = len(graph)
        min_rep = float('inf')
        for perm in itertools.permutations(range(n)):
            rep = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if graph[i][j] and perm[i] > perm[j]:
                        rep += 1
            min_rep = min(min_rep, rep)
        return min_rep
    
    def resolution_proof_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
            clauses.append([-i - 1])
        for u, v in graph:
            clauses.append([-u - 1, v + 1])
            clauses.append([-v - 1, u + 1])
        
        def dpll(clauses, assignment, unit_clause):
            if not clauses:
                return True
            if unit_clause:
                literal = unit_clause[0]
                if literal > 0:
                    assignment[literal] = True
                else:
                    assignment[-literal] = False
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, assignment, None)
            
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                unit_clause = unit_clauses[0]
                return dpll(clauses, assignment, unit_clause)
            
            literal = next(l for l in range(1, n + 1) if l not in assignment and -l not in assignment)
            if literal > 0:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll(clauses, new_assignment, None):
                    return True
                new_assignment[literal] = False
                new_assignment[-literal] = True
                if dpll(clauses, new_assignment, None):
                    return True
            else:
                new_assignment = assignment.copy()
                new_assignment[-literal] = True
                if dpll(clauses, new_assignment, None):
                    return True
                new_assignment[-literal] = False
                new_assignment[literal] = True
                if dpll(clauses, new_assignment, None):
                    return True
            
            return False
        
        assignment = [False] * (n + 1)
        width = 0
        while not dpll(clauses, assignment, None):
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal > 0:
                    assignment[literal] = True
                else:
                    assignment[-literal] = False
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                clauses = new_clauses
                width += 1
            else:
                break
        
        return width
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, 41):
        for _ in range(30 // (n - 4)):
            graph = generate_d_regular_graph(n, random.randint(2, min(n // 2 - 1, 4)))
            if not graph or not is_connected(graph):
                continue
            instances_tested += 1
            qcr_G = find_minimal_representation(graph)
            w_phi_G = resolution_proof_width(graph)
            metric_values.append((qcr_G, w_phi_G))
    
    if not metric_values:
        return {
            "metric_name": "qcr(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    qcr_values, w_phi_values = zip(*metric_values)
    mean_qcr = sum(qcr_values) / len(qcr_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    std_qcr = math.sqrt(sum((x - mean_qcr) ** 2 for x in qcr_values) / len(qcr_values))
    std_w_phi = math.sqrt(sum((x - mean_w_phi) ** 2 for x in w_phi_values) / len(w_phi_values))
    
    correlation_coefficient = sum((qcr_values[i] - mean_qcr) * (w_phi_values[i] - mean_w_phi) for i in range(len(qcr_values))) / (len(qcr_values) * std_qcr * std_w_phi)
    
    return {
        "metric_name": "qcr(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 3 * (std_qcr / len(qcr_values)) and abs(correlation_coefficient) >= 3 * (std_w_phi / len(w_phi_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")