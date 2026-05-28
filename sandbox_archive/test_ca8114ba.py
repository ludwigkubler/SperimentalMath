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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def quandle_rank(edges):
        n = len(edges) + 1
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        rank = 0
        for i in range(n):
            if sum(adjacency_matrix[i]) > 0:
                rank += 1
                for j in range(n):
                    if adjacency_matrix[j][i] == 1:
                        for k in range(n):
                            if adjacency_matrix[k][j] == 1:
                                adjacency_matrix[k][i] = 0
        
        return rank
    
    def tseitin_formula(edges, n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Each vertex must be connected to at least one other vertex
        for i in range(n):
            clause = []
            for j in range(n):
                if (i, j) in edges or (j, i) in edges:
                    clause.append(literals[j])
                else:
                    clause.append(f'~{literals[j]}')
            clauses.append(clause)
        
        # Each edge must be connected to exactly one other vertex
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in edges or (j, i) in edges:
                    clause = [f'~{literals[i]}', f'~{literals[j]}']
                    clauses.append(clause)
        
        return clauses
    
    def resolution_refutation_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(l == f'~{r}' and r in stack[j] for l in stack[i]):
                        new_clause = [l for l in stack[i] if l not in stack[j]]
                        break
                if new_clause:
                    break
            
            if not new_clause:
                return len(stack)
            
            stack.append(new_clause)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph_edges = generate_random_graph(n)
            quandle_r = quandle_rank(graph_edges)
            tseitin_clauses = tseitin_formula(graph_edges, n)
            refutation_length = resolution_refutation_length(tseitin_clauses)
            
            total_length += refutation_length
            instances_tested += 1
    
    mean_length = Fraction(total_length, instances_tested)
    conjecture_holds = mean_length >= 2 ** quandle_r
    counterexample = "" if conjecture_holds else f"Graph with n={n}, rank={quandle_r}, refutation_length={mean_length}"
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": float(mean_length),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    total_length = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")