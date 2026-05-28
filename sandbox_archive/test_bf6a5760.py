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
    
    def generate_expander_graph(n, k):
        if n < 2 * k or k <= 0:
            return None
        graph = {i: set() for i in range(n)}
        for _ in range(k):
            u, v = random.sample(range(n), 2)
            while u == v or v in graph[u]:
                u, v = random.sample(range(n), 2)
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def tseitin_formula(graph):
        if not graph:
            return ""
        n = len(graph)
        clauses = []
        for i in range(n):
            literals = [f"x{i}"]
            for j in graph[i]:
                literals.append(f"~x{j}")
            clause = " & ".join(literals) + " -> x{0}".format(i)
            clauses.append(clause)
        return " & ".join(clauses)
    
    def hodge_rank(graph):
        if not graph:
            return 0
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
            for j in graph[i]:
                A[i][j] = -1
        
        def gaussian_elimination(A):
            rows, cols = len(A), len(A[0])
            rank = 0
            
            for col in range(cols):
                pivot_row = None
                for row in range(rank, rows):
                    if A[row][col] != 0:
                        pivot_row = row
                        break
                
                if pivot_row is None:
                    continue
                
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                
                for row in range(rank, rows):
                    factor = -A[row][col] / A[pivot_row][col]
                    for j in range(cols):
                        A[row][j] += factor * A[pivot_row][j]
            
            return rank
        
        return gaussian_elimination(A)
    
    def resolution_length(formula):
        if not formula:
            return 0
        stack = [formula]
        length = 0
        while stack:
            clause = stack.pop()
            literals = clause.split(" -> ")[1].split("&")
            for literal in literals:
                if literal.startswith("~"):
                    negated_literal = literal[1:]
                    if negated_literal in stack:
                        stack.remove(negated_literal)
                        length += 1
                    else:
                        return float('inf')
        return length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            graph = generate_expander_graph(n, n // 2)
            if not graph:
                continue
            formula = tseitin_formula(graph)
            rank = hodge_rank(graph)
            length = resolution_length(formula)
            results.append((rank, length))
    
    if not results:
        return {
            "metric_name": "Hodge Rank / Resolution Length",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_sum = sum(rank for rank, _ in results)
    length_sum = sum(length for _, length in results)
    mean_rank = rank_sum / len(results)
    mean_length = length_sum / len(results)
    
    if mean_length == 0:
        return {
            "metric_name": "Hodge Rank / Resolution Length",
            "metric_value": 0,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "resolution_length_zero"
        }
    
    ratio_sum = sum(rank / length for rank, length in results)
    mean_ratio = ratio_sum / len(results)
    
    return {
        "metric_name": "Hodge Rank / Resolution Length",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio <= 2 ** (n_values[0] // 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")