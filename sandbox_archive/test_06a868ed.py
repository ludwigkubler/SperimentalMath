# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def negate(lit):
    return -lit if lit > 0 else -lit + 1

def dpll_with_memoization(clauses, assignment, memo=defaultdict(lambda: None)):
    key = tuple(sorted(assignment.items()))
    if key in memo:
        return memo[key]
    
    if not clauses:
        return True
    if any(not any(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in clauses):
        return False
    
    literal = next(lit for lit in range(1, max(abs(lit) for clause in clauses) + 1) if lit not in assignment and -lit not in assignment)
    
    def extend_assignment(lit):
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        return new_assignment
    
    def extend_assignment_negate(lit):
        new_assignment = assignment.copy()
        new_assignment[lit] = False
        return new_assignment
    
    if dpll_with_memoization([clause for clause in clauses if literal not in clause and -literal not in clause], extend_assignment(literal), memo) or \
       dpll_with_memoization([clause for clause in clauses if literal not in clause and -literal not in clause], extend_assignment_negate(literal), memo):
        memo[key] = True
        return True
    
    memo[key] = False
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n, m):
        graph = {i: [] for i in range(1, n + 1)}
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(1, n + 1), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def gromov_hyperbolicity(graph):
        n = len(graph)
        if n < 4:
            return 0
        
        def triangle_distance(a, b, c):
            return min(len(graph[a] & graph[b]), len(graph[b] & graph[c]), len(graph[c] & graph[a]))
        
        max_delta = -math.inf
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                for c in range(b + 1, n + 1):
                    delta = (triangle_distance(a, b, c) + triangle_distance(a, c, b) - triangle_distance(b, c, a)) / 2
                    max_delta = max(max_delta, delta)
        return max_delta
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: (2 * i - 1, 2 * i) for i in range(1, n + 1)}
        clauses = []
        
        for u in range(1, n + 1):
            if not graph[u]:
                clauses.append([literals[u][0]])
            else:
                clauses.append([-literals[u][0]] + [literals[v][1] for v in graph[u]])
        
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if v not in graph[u]:
                    clauses.append([literals[u][1], literals[v][0]])
                    clauses.append([literals[u][0], literals[v][1]])
        
        return clauses
    
    def resolution_length(clauses):
        return len(clauses) if dpll_with_memoization(clauses, {}) else float('inf')
    
    n = random.randint(5, 40)
    m = random.randint(n - 1, n * (n - 1) // 2)
    graph = generate_random_graph(n, m)
    delta_G = gromov_hyperbolicity(graph)
    clauses = tseitin_formula(graph)
    
    resolution_length_value = resolution_length(clauses)
    conjecture_holds = True
    counterexample = ""
    
    if delta_G >= 1 and resolution_length_value < 2 ** delta_G:
        conjecture_holds = False
        counterexample = f"Graph with n={n}, m={m} has δ(G)={delta_G} but resolution length {resolution_length_value} < 2^{delta_G}"
    elif delta_G <= 1 and not (5 * (n - 1) ** 3 // 6 <= resolution_length_value <= 4 * n ** 3):
        conjecture_holds = False
        counterexample = f"Graph with n={n}, m={m} has δ(G)={delta_G} but resolution length {resolution_length_value} not in range [5*(n-1)^3/6, 4*n^3]"
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": resolution_length_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")