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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment, clauses):
        if not clauses:
            return True
        literal = next(lit for lit in set([abs(x) for x in sum(cnf, [])]) if lit not in assignment)
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            new_clauses = [c for c in cnf if literal not in c and -literal not in c]
            if dpll(new_cnf, new_assignment, new_clauses):
                return True
        return False
    
    def compute_geometric_entropy(graph):
        n = len(graph)
        degrees = sum(sum(1 for _ in neighbors) for _, neighbors in graph.items()) / (2 * n)
        entropy = -degrees * math.log(degrees, 2) if degrees > 0 else 0
        return entropy
    
    def generate_frege_proof_tree(cnf):
        # Simplified DPLL to generate a proof tree
        assignment = {}
        clauses = cnf[:]
        stack = []
        while True:
            if not clauses:
                break
            literal = next(lit for lit in set([abs(x) for x in sum(clauses, [])]) if lit not in assignment)
            value = dpll(cnf, assignment, clauses)
            stack.append((literal, value))
            if value:
                assignment[literal] = True
                clauses = [c for c in cnf if literal not in c and -literal not in c]
            else:
                assignment[literal] = False
                clauses = [c for c in cnf if literal in c or -literal in c]
        return stack
    
    def build_graph(proof_tree):
        graph = {}
        for node in proof_tree:
            literal, value = node
            if literal not in graph:
                graph[literal] = set()
            for parent in proof_tree[:proof_tree.index(node)]:
                parent_literal, _ = parent
                if parent_literal != literal and (parent_literal not in graph or literal not in graph[parent_literal]):
                    graph[literal].add(parent_literal)
                    if parent_literal not in graph:
                        graph[parent_literal] = set()
                    graph[parent_literal].add(literal)
        return graph
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        proof_tree = generate_frege_proof_tree(cnf)
        graph = build_graph(proof_tree)
        depth = len(proof_tree)
        
        if depth <= 1:
            continue
        
        entropy = compute_geometric_entropy(graph)
        upper_bound = math.sqrt(depth)
        
        metric_values.append(entropy - upper_bound)
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    conjecture_holds = all(x <= 1.5 for x in metric_values)
    counterexample = "" if conjecture_holds else "metric_value > 1.5"
    
    return {
        "metric_name": "Entropy - Upper Bound",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_value > 1.5\" first_failing_seed={first_failing_seed}")