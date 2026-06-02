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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        degree_counts = [0] * n
        edges_added = set()
        
        for _ in range(k * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added.add((u, v))
                break
        
        for i in range(n):
            if degree_counts[i] != k:
                return None
        return graph
    
    def tseitin_encoding(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        
        return clauses
    
    def frege_proof_length(clauses):
        n = len(clauses)
        proof = []
        
        for i in range(n):
            for literal in clauses[i]:
                if literal.startswith('-'):
                    negated_literal = literal[1:]
                    if negated_literal not in proof:
                        proof.append(negated_literal)
                else:
                    if literal not in proof:
                        proof.append(literal)
        
        return len(proof)
    
    def minimal_twisted_module_order(clauses):
        n = len(clauses)
        order = 0
        
        for i in range(n):
            for clause in clauses:
                if literal in clause:
                    order += 1
                    break
        
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_length = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_k_regular_graph(n, 2)
            if graph is None:
                continue
            
            clauses = tseitin_encoding(graph)
            length = frege_proof_length(clauses)
            order = minimal_twisted_module_order(clauses)
            
            total_order += order
            total_length += length
            instances_tested += 1
            max_n = max(max_n, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = total_order / instances_tested
    mean_length = total_length / instances_tested
    
    correlation_coefficient = (instances_tested * mean_order * mean_length - 
                               sum(order * length for order, length in zip(clauses, clauses))) / \
                              math.sqrt((instances_tested * sum(order**2 for order in clauses) - 
                                          sum(order**2 for order in clauses)) * 
                                        (instances_tested * sum(length**2 for length in clauses) - 
                                         sum(length**2 for length in clauses)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")