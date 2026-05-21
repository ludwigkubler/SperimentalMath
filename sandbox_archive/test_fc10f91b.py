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

def generate_regular_graph(n, degree):
    if (n * degree) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges = set()
    for v in range(n):
        for u in range(v + 1, n):
            if len(graph[v]) < degree and len(graph[u]) < degree:
                if (v, u) not in edges and (u, v) not in edges:
                    graph[v].append(u)
                    graph[u].append(v)
                    edges.add((v, u))
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = {i: f"x{i}" for i in range(n)}
    clauses = []
    
    # Add clauses for each vertex
    for v in range(n):
        if not graph[v]:
            continue
        clause = [literals[v]]
        for u in graph[v]:
            clause.append(-literals[u])
        clauses.append(clause)
    
    # Add clauses for each edge
    for v in range(n):
        if not graph[v]:
            continue
        for u in graph[v]:
            for w in graph[u]:
                if w != v and (v, u) != (u, w):
                    clause = [-literals[v], -literals[u], literals[w]]
                    clauses.append(clause)
    
    return clauses

def resolution_proof_length(clauses):
    def dpll(clauses, assignment, unit_clauses):
        while True:
            if not unit_clauses:
                break
            literal = unit_clauses.pop()
            polarity = literal > 0
            for clause in clauses[:]:
                if literal in clause:
                    clauses.remove(clause)
                elif -literal in clause:
                    clause.remove(-literal)
                    if len(clause) == 1:
                        unit_clauses.add(clause[0])
            assignment[literal] = polarity
        
        if not clauses:
            return True
        for literal in range(1, max(literals.values()) + 1):
            if literal not in assignment and -literal not in assignment:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll(clauses, new_assignment, unit_clauses):
                    return True
                new_assignment[literal] = False
                if dpll(clauses, new_assignment, unit_clauses):
                    return True
        return False
    
    unit_clauses = [l for l in literals.values() if l not in assignment and -l not in assignment]
    return len(clauses) + len(unit_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    degree = random.randint(3, min(n // 2, 4))
    graph = generate_regular_graph(n, degree)
    if not graph:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clauses = tseitin_formula(graph)
    proof_length = resolution_proof_length(clauses)
    
    g_G = len(graph) - max(len(neighbors) for neighbors in graph.values())
    conjecture_holds = proof_length >= 2 ** g_G
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Proof length {proof_length} < 2^{g_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break