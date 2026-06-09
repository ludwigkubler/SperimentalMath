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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    return A

def rank(A):
    n = len(A)
    r = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(n)):
            continue
        r += 1
    return r

def dpll_tree_height(graph, assignment=[]):
    if not graph:
        return len(assignment)
    
    node = next(iter(graph))
    neighbors = graph[node]
    remaining_graph = {n: g.copy() for n, g in graph.items() if n != node}
    
    for neighbor in neighbors:
        if neighbor in assignment and assignment[neighbor] == 0:
            continue
        new_assignment = assignment + [(node, 1), (neighbor, 0)]
        height = dpll_tree_height(remaining_graph, new_assignment)
        if height > 0:
            return height
    
    for neighbor in neighbors:
        if neighbor in assignment and assignment[neighbor] == 1:
            continue
        new_assignment = assignment + [(node, 0), (neighbor, 1)]
        height = dpll_tree_height(remaining_graph, new_assignment)
        if height > 0:
            return height
    
    return 0

def min_categorical_dimension(graph):
    n = len(graph)
    A = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            if (i, j) in graph and (j, i) in graph:
                A[i][j] = 1
                A[j][i] = 1
    
    return rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        graph = {}
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    graph[(i, j)] = True
                    graph[(j, i)] = True
        
        min_dim = min_categorical_dimension(graph)
        height = dpll_tree_height(graph)
        
        instances_tested += 1
        total_metric_value += abs(min_dim - height)
        
        if n > n_max:
            n_max = n
        
        if abs(min_dim - height) > 3:
            conjecture_holds = False
            counterexample = f"n={n}, min_dim={min_dim}, height={height}"
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")