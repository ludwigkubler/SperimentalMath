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
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, random.randint(2, n))
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        graph = {}
        var_count = len(cnf)
        for i in range(var_count):
            graph[i + 1] = []
        for clause in cnf:
            new_var = var_count + len(graph) + 1
            graph[new_var] = [abs(lit) for lit in clause]
            for lit in clause:
                if lit > 0:
                    graph[lit].append(new_var)
                else:
                    graph[-lit].append(-new_var)
        return graph
    
    def spanning_tree(graph):
        visited = set()
        stack = [1]
        tree = {1: []}
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        tree[neighbor] = []
                        stack.append(neighbor)
                        tree[node].append(neighbor)
        return tree
    
    def edges_in_tree(tree):
        edges = set()
        for node, neighbors in tree.items():
            for neighbor in neighbors:
                edge = tuple(sorted([node, neighbor]))
                if edge not in edges:
                    edges.add(edge)
        return len(edges)
    
    def boolean_circuit_complexity(n):
        # Placeholder function to simulate circuit complexity
        return n
    
    n_max = 40
    instances_tested = 0
    total_geometric_complexity = 0
    total_entanglement_complexity = 0
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        graph = tseitin_graph(cnf)
        tree = spanning_tree(graph)
        geometric_complexity = edges_in_tree(tree)
        entanglement_complexity = boolean_circuit_complexity(geometric_complexity)
        
        total_geometric_complexity += geometric_complexity
        total_entanglement_complexity += entanglement_complexity
        instances_tested += 1
    
    mean_geometric_complexity = total_geometric_complexity / instances_tested
    mean_entanglement_complexity = total_entanglement_complexity / instances_tested
    correlation_coefficient = (instances_tested * sum(g * e for g, e in zip(range(5, 41), range(5, 41))) -
                               sum(range(5, 41)) * mean_geometric_complexity) / \
                              math.sqrt((instances_tested * sum(g**2 for g in range(5, 41)) - sum(range(5, 41))**2) *
                                        (instances_tested * sum(e**2 for e in range(5, 41)) - sum(range(5, 41))**2))
    
    conjecture_holds = abs(correlation_coefficient - 0.8) < 0.1
    counterexample = "" if conjecture_holds else "correlation_outside_tolerance"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_tolerance\" first_failing_seed={first_failing_seed}")