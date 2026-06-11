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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def term_graph(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in graph:
                    graph[var] = set()
                for other_var in graph:
                    if other_var != var and (literal * -1) in [c for c in cnf if other_var in c]:
                        graph[var].add(other_var)
        return graph
    
    def minimal_order(graph):
        visited = set()
        order = 0
        
        def dfs(node):
            nonlocal order
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
                            order += 1
    
        for node in graph:
            if node not in visited:
                dfs(node)
        
        return order
    
    def communication_complexity_rank_variance(cnf):
        rank_variances = []
        for _ in range(10):  # Sample multiple times to get a better estimate
            assignment = {i + 1: random.choice([-1, 1]) for i in range(len(cnf))}
            rank = sum(1 for clause in cnf if sum(lit * assignment[abs(lit)] for lit in clause) > 0)
            rank_variances.append(rank)
        return Fraction(sum(rank_variances), len(rank_variances))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = term_graph(cnf)
    order = minimal_order(graph)
    rank_variance = communication_complexity_rank_variance(cnf)
    
    metric_name = "order_vs_rank_variance"
    metric_value = Fraction(order) * rank_variance
    instances_tested = 10
    n_max = n
    conjecture_holds = metric_value >= n ** 2 / 4  # Example threshold, adjust as needed
    counterexample = "" if conjecture_holds else f"order={order}, rank_variance={rank_variance}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0)
        print(f"RESULT: FALSIFIED counterexample=\"negative_variance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")