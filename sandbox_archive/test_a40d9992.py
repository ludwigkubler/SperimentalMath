# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_tseitin_formula(n):
    if n < 1:
        return "", []
    
    variables = [f'x{i}' for i in range(1, 2*n)]
    clauses = []
    
    # Generate OR clauses
    for i in range(1, n+1):
        clause = f'{variables[i-1]} | {variables[2*i-1]}'
        clauses.append(clause)
        
    # Generate AND clauses
    for i in range(1, n+1):
        clause = f'~{variables[i-1]} & ~{variables[2*i-1]} | ~{variables[2*i-2]}'
        clauses.append(clause)
    
    # Final OR clause
    final_clause = ' | '.join(variables[:n])
    clauses.append(final_clause)
    
    formula = ' & '.join(clauses)
    return formula, variables

def generate_random_graph(n):
    graph = [[] for _ in range(n)]
    edges = set()
    
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                graph[i].append(j)
                graph[j].append(i)
                edges.add((i, j))
    
    return graph

def tree_width(graph):
    def dfs(node, parent):
        max_depth = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                depth = dfs(neighbor, node) + 1
                max_depth = max(max_depth, depth)
        return max_depth
    
    n = len(graph)
    max_width = 0
    
    for i in range(n):
        width = dfs(i, -1)
        max_width = max(max_width, width)
    
    return max_width

def unitary_representation(graph):
    n = len(graph)
    U = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        U[i][i] = Fraction(1)
    
    for i in range(n):
        for j in range(i+1, n):
            if j in graph[i]:
                U[i][j] = Fraction(1)
                U[j][i] = Fraction(1)
    
    return U

def min_rank(matrix):
    n = len(matrix)
    rank = 0
    
    for i in range(n):
        pivot_row = -1
        for j in range(i, n):
            if matrix[j][i] != Fraction(0):
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        rank += 1
        
        for j in range(n):
            if j != i:
                factor = matrix[j][i] / matrix[pivot_row][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[pivot_row][k]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula, variables = generate_tseitin_formula(n)
        graph = generate_random_graph(n)
        
        if not graph or len(graph) != n:
            continue
        
        tw = tree_width(graph)
        U = unitary_representation(graph)
        min_rank_U = min_rank(U)
        
        results.append({
            "n": n,
            "tw": tw,
            "min_rank_U": min_rank_U
        })
    
    if not results:
        return {
            "metric_name": "min_rank_U",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_tw = sum(result["tw"] for result in results)
    total_min_rank_U = sum(result["min_rank_U"] for result in results)
    instances_tested = len(results)
    
    mean_tw = Fraction(total_tw, instances_tested)
    mean_min_rank_U = Fraction(total_min_rank_U, instances_tested)
    
    conjecture_holds = all(min_rank_U <= 2 * tw for result in results)
    counterexample = "" if conjecture_holds else "min_rank_U > 2 * tw"
    
    return {
        "metric_name": "min_rank_U",
        "metric_value": mean_min_rank_U,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not results:
            results.append(trial_result)
        else:
            results[-1]["instances_tested"] += trial_result["instances_tested"]
            results[-1]["metric_value"] += trial_result["metric_value"]
    
    total_metric_value = sum(result["metric_value"] for result in results)
    instances_tested = sum(result["instances_tested"] for result in results)
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_U > 2 * tw\" first_failing_seed={first_failing_seed}")