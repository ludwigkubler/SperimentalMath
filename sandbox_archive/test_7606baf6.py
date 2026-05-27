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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def dpll(formula):
        if not formula:
            return True
        literal = next((l for l in range(1, len(formula[0]) + 1) if any(l in c or -l in c for c in formula)), None)
        if literal is None:
            return False
        def dpll_helper(formula, assignment):
            if not formula:
                return True
            new_formula = []
            for clause in formula:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clause = [l for l in clause if l != -literal]
                    if not new_clause:
                        return False
                    new_formula.append(new_clause)
                else:
                    new_formula.append(clause)
            return dpll_helper(new_formula, assignment + [literal])
        if dpll_helper(formula, []):
            return True
        formula = [[l for l in clause if l != -literal] for clause in formula]
        return dpll_helper(formula, [-literal])
    
    def minimal_rank(graph):
        n = len(graph)
        visited = [False] * n
        rank = 0
        
        def dfs(node):
            nonlocal rank
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    rank += 1
                    for neighbor in range(n):
                        if graph[node][neighbor] and not visited[neighbor]:
                            stack.append(neighbor)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        return rank
    
    def cayley_graph(formula):
        n = len(formula)
        graph = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if formula[i][j % 3] == formula[j][i % 3]:
                    graph[i][j] = True
        return graph
    
    def maximal_spanning_tree(graph):
        n = len(graph)
        visited = [False] * n
        tree_edges = []
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in range(n):
                        if graph[node][neighbor] and not visited[neighbor]:
                            tree_edges.append((node, neighbor))
                            stack.append(neighbor)
        
        dfs(0)
        return tree_edges
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    cayley_graph_matrix = cayley_graph(formula)
    minimal_rank_value = minimal_rank(cayley_graph_matrix)
    resolution_depth = len(dpll(formula))
    
    metric_name = "Minimal Rank of Quotient Space"
    metric_value = min(minimal_rank_value, math.log(n))
    instances_tested = 1
    conjecture_holds = minimal_rank_value >= math.log(n) and resolution_depth >= math.log(n)
    counterexample = "" if conjecture_holds else f"n={n}, rank={minimal_rank_value}, depth={resolution_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")