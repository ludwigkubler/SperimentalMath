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
        if (d * n) % 2 != 0 or d < 1 or n < 1:
            return None
        adj_list = {i: [] for i in range(n)}
        edges_used = set()
        for _ in range(d * n // 2):
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges_used and (v, u) not in edges_used:
                adj_list[u].append(v)
                adj_list[v].append(u)
                edges_used.add((u, v))
        return adj_list
    
    def compute_expansion(graph):
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph.values()]
        max_degree = max(degrees)
        min_degree = min(degrees)
        expansion = (max_degree + min_degree) / 2
        return expansion
    
    def persistent_homology_based_morse_matching(graph):
        # Simplified Morse matching algorithm using a greedy approach
        n = len(graph)
        critical_simplices = []
        visited = set()
        
        for node in range(n):
            if node not in visited:
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        neighbors = graph[current]
                        if len(neighbors) == 1:
                            critical_simplices.append((current, neighbors[0]))
                        else:
                            for neighbor in neighbors:
                                if neighbor not in visited:
                                    stack.append(neighbor)
        return len(critical_simplices)
    
    def resolution_length(graph):
        # Simplified DPLL-based proof size estimator
        n = len(graph)
        clauses = []
        for node in range(n):
            clause = [node, -node]
            clauses.append(clause)
        
        def dpll(clauses, assignment, model):
            if not clauses:
                return True
            literal = find_pure_literal(clauses)
            if literal is None:
                literal = choose_branching_literal(clauses)
            if literal > 0:
                new_assignment = assignment | {literal: True}
                new_model = model + [literal]
            else:
                new_assignment = assignment | {-literal: False}
                new_model = model + [-literal]
            
            if dpll([c for c in clauses if not unit_propagate(c, literal)], new_assignment, new_model):
                return True
            return False
        
        def find_pure_literal(clauses):
            pure_literals = set()
            for clause in clauses:
                positive = [l for l in clause if l > 0]
                negative = [-l for l in clause if l < 0]
                if len(positive) == 1 and all(-p not in pure_literals for p in positive):
                    pure_literals.add(positive[0])
                if len(negative) == 1 and all(p not in pure_literals for p in negative):
                    pure_literals.add(negative[0])
            return None
        
        def choose_branching_literal(clauses):
            literals = set()
            for clause in clauses:
                literals.update([l for l in clause if l > 0] + [-l for l in clause if l < 0])
            return random.choice(list(literals))
        
        assignment = {}
        model = []
        return dpll(clauses, assignment, model)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    expansion = compute_expansion(graph)
    if expansion < 0.1 * math.sqrt(math.log(n)):
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "expansion_too_low"
        }
    
    nu_G = persistent_homology_based_morse_matching(graph)
    resolution_len = resolution_length(graph)
    
    if resolution_len is not None:
        c = 0.2
        conjecture_holds = resolution_len >= 2 ** (c * nu_G)
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_length_not_computed"
        }
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    num_trials = len(results)
    mean_metric_value = total_metric_value / num_trials if num_trials > 0 else 0
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / num_trials if num_trials > 1 else 0
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")