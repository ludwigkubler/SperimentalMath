# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate OR clauses for each variable
        for var in variables:
            clause = [var]
            for other_var in variables:
                if other_var != var:
                    clause.append(-other_var)
            clauses.append(clause)
        
        # Generate AND clauses for all pairs of variables
        for var1, var2 in combinations(variables, 2):
            clause = [-var1, -var2]
            clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        literals = set()
        queue = []
        
        def add_clause(clause):
            for literal in clause:
                if literal not in literals and -literal not in literals:
                    literals.add(literal)
                    queue.append(literal)
        
        for clause in clauses:
            add_clause(clause)
        
        while queue:
            literal = queue.pop()
            if literal > 0:
                neg_literal = -literal
            else:
                neg_literal = -literal
            
            new_clauses = []
            for clause in clauses:
                if neg_literal in clause:
                    continue
                if -neg_literal in clause:
                    clause.remove(-neg_literal)
                    if not clause:
                        return len(literals)
                    new_clauses.append(clause)
                else:
                    new_clauses.append(clause + [neg_literal])
            
            for new_clause in new_clauses:
                add_clause(new_clause)
        
        return len(literals)
    
    def persistent_homology(graph):
        # Simplified version of persistent homology using a greedy algorithm
        components = {}
        for node in graph:
            if node not in components:
                component_id = max(components.values()) + 1 if components else 0
                stack = [node]
                while stack:
                    current_node = stack.pop()
                    if current_node not in components:
                        components[current_node] = component_id
                        for neighbor in graph[current_node]:
                            if neighbor not in components:
                                stack.append(neighbor)
        return len(components)
    
    def generate_graph(clauses):
        graph = {}
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    var = literal
                else:
                    var = -literal
                
                if var not in graph:
                    graph[var] = []
                
                for other_var in set(clause) - {literal}:
                    if other_var > 0:
                        neighbor = other_var
                    else:
                        neighbor = -other_var
                    
                    if neighbor not in graph[var]:
                        graph[var].append(neighbor)
        
        return graph
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4)):
            clauses = generate_tseitin_formula(n)
            graph = generate_graph(clauses)
            w_phi = resolution_width(clauses)
            C_phi = persistent_homology(graph)
            
            metric_values.append((w_phi, C_phi))
    
    correlation_coefficient = sum((x[0] * x[1] for x in metric_values)) / len(metric_values)
    mean_value = sum(x[0] for x in metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x[0] - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = correlation_coefficient < -0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_dev, support_fraction))
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")