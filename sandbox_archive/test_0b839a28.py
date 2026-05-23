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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append((i,))
            for j in range(i + 1, n + 1):
                clauses.append((i, -j))
                clauses.append((-i, j))
        return variables, clauses
    
    def is_expander_graph(n, edges):
        adjacency_list = [[] for _ in range(n)]
        for u, v in edges:
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)
        
        min_degree = float('inf')
        max_degree = 0
        for i in range(n):
            degree = len(adjacency_list[i])
            if degree < min_degree:
                min_degree = degree
            if degree > max_degree:
                max_degree = degree
        
        return (max_degree - min_degree) / min_degree >= 1
    
    def compute_min_local_curvature(n, edges):
        adjacency_list = [[] for _ in range(n)]
        for u, v in edges:
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)
        
        n_edges = len(edges)
        if n_edges == 0:
            return 1
        
        min_curvature = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                neighbors_i = set(adjacency_list[i])
                neighbors_j = set(adjacency_list[j])
                common_neighbors = len(neighbors_i & neighbors_j)
                if common_neighbors == 0:
                    curvature = float('inf')
                else:
                    curvature = (len(neighbors_i) + len(neighbors_j)) / (2 * common_neighbors)
                if curvature < min_curvature:
                    min_curvature = curvature
        
        return min_curvature
    
    def resolution_prover(n, clauses):
        stack = []
        literals = set(range(1, n + 1))
        
        while literals and stack:
            literal = random.choice(list(literals))
            literals.remove(abs(literal))
            
            if literal > 0:
                for clause in clauses:
                    if literal in clause:
                        clauses.remove(clause)
                    elif -literal in clause:
                        clause.remove(-literal)
                        if len(clause) == 1:
                            stack.append(clause[0])
                            break
            else:
                for clause in clauses:
                    if -literal in clause:
                        clauses.remove(clause)
                    elif literal in clause:
                        clause.remove(literal)
                        if len(clause) == 1:
                            stack.append(-clause[0])
                            break
        
        return len(stack)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if is_expander_graph(n, edges):
        min_curvature = compute_min_local_curvature(n, edges)
    else:
        min_curvature = 1
    
    resolution_length = resolution_prover(n, clauses)
    
    metric_value = resolution_length / (2 ** math.ceil(math.log2(min_curvature)))
    conjecture_holds = metric_value >= 0.5
    counterexample = "" if conjecture_holds else f"Non-expander graph with n={n}"
    
    return {
        "metric_name": "Resolution Proof Length / 2^Ω(Min Local Curvature)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-expander graph\" first_failing_seed={first_failing_seed}")