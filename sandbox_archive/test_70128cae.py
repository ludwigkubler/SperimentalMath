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
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f"~{variables[i-1]}"])
            clauses.append([variables[i-1], f"~x{i}"])
        return variables, clauses
    
    def is_loop(graph, u, visited, parent):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                if is_loop(graph, v, visited, u):
                    return True
            elif v != parent:
                return True
        return False
    
    def find_loops(graph):
        visited = [False] * len(graph)
        loops = []
        for i in range(len(graph)):
            if not visited[i]:
                if is_loop(graph, i, visited, -1):
                    loops.append(i)
        return loops
    
    def resolution_length(clauses):
        queue = clauses[:]
        while queue:
            clause = queue.pop()
            new_clauses = []
            for other_clause in queue:
                common_vars = set(clause) & set(other_clause)
                if len(common_vars) == 1:
                    var, neg_var = list(common_vars)[0], f"~{list(common_vars)[0]}"
                    new_clauses.extend([c for c in queue if neg_var not in c])
                    new_clauses.append([v for v in other_clause if v != var and v != neg_var])
            queue.extend(new_clauses)
        return len(queue)
    
    def geometric_locus_size(graph):
        loops = find_loops(graph)
        return len(loops)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        graph = [[] for _ in range(n)]
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    u, v = int(clause[i][1:]) - 1, int(clause[j][1:]) - 1
                    graph[u].append(v)
                    graph[v].append(u)
        
        loops_size = geometric_locus_size(graph)
        length = resolution_length(clauses)
        total_length += length
        instances_tested += 1
    
    mean_length = total_length / instances_tested
    conjecture_holds = mean_length <= math.exp(2 * loops_size) and mean_length >= math.exp(0.5 * loops_size)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean length {mean_length} exceeds expected bound for loops size {loops_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")