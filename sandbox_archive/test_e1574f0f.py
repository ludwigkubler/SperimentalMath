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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[] for _ in range(n)]
    degree_count = [0] * n
    edges_added = set()
    
    while sum(degree_count) < n * d:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u == v or (u, v) in edges_added or (v, u) in edges_added:
            continue
        graph[u].append(v)
        graph[v].append(u)
        degree_count[u] += 1
        degree_count[v] += 1
        edges_added.add((u, v))
    
    return graph

def is_valid_assignment(assignment, clauses):
    for clause in clauses:
        if not any(assignment[i] == (not literal) for i, literal in enumerate(clause)):
            return False
    return True

def resolution_proof_width(graph):
    n = len(graph)
    clauses = []
    
    # Convert graph to CNF form (simplified example)
    for u in range(n):
        for v in range(u + 1, n):
            if v not in graph[u]:
                clauses.append([u, -v])
                clauses.append([-u, v])
    
    assignments = [False] * n
    assignment_stack = []
    
    while True:
        assignment_found = False
        for clause in clauses:
            if all(not assignment[i] == (not literal) for i, literal in enumerate(clause)):
                assignment_found = True
                break
        
        if not assignment_found:
            return len(assignment_stack)
        
        unit_clause = None
        for i, clause in enumerate(clauses):
            if sum(literal != 0 for literal in clause) == 1:
                unit_clause = clause
                break
        
        if unit_clause is None:
            return len(assignment_stack)
        
        literal = next(literal for literal in unit_clause if literal != 0)
        assignment[labs(literal) - 1] = literal > 0
        
        if literal < 0:
            literal = -literal
            for clause in clauses:
                if literal in clause:
                    clause.remove(literal)
                elif -literal in clause:
                    clause.remove(-literal)
        
        assignment_stack.append((unit_clause, literal))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    qcr_values = []
    w_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            d = random.randint(2, min(n // 2 - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            
            clauses = []
            for u in range(n):
                for v in range(u + 1, n):
                    if v not in graph[u]:
                        clauses.append([u, -v])
                        clauses.append([-u, v])
            
            qcr_value = len(clauses) / (n * d)
            w_value = resolution_proof_width(graph)
            
            qcr_values.append(qcr_value)
            w_values.append(w_value)
            instances_tested += 1
    
    if not qcr_values or not w_values:
        return {
            "metric_name": "qcr(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_qcr = sum(qcr_values) / len(qcr_values)
    mean_w = sum(w_values) / len(w_values)
    std_qcr = math.sqrt(sum((x - mean_qcr) ** 2 for x in qcr_values) / len(qcr_values))
    std_w = math.sqrt(sum((x - mean_w) ** 2 for x in w_values) / len(w_values))
    
    correlation_coefficient = sum((qcr_values[i] - mean_qcr) * (w_values[i] - mean_w) for i in range(len(qcr_values))) / (len(qcr_values) * std_qcr * std_w)
    
    if abs(correlation_coefficient) > 0.97:
        return {
            "metric_name": "qcr(G)",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "qcr(G)",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")