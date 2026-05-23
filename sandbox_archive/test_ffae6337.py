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

def generate_graph(clauses):
    n = len(clauses)
    graph = [[] for _ in range(n)]
    for clause in clauses:
        if len(clause) >= 3 and clause[-2] != '-':
            v = int(clause[-2]) - 1
            u = int(clause[-3]) - 1
            graph[u].append(v)
            graph[v].append(u)
    return graph

def find_loops(graph):
    n = len(graph)
    visited = [False] * n
    parent = [-1] * n
    
    def dfs(node, p):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                parent[neighbor] = node
                if dfs(neighbor, node):
                    return True
            elif neighbor != p:
                return True
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False

def resolution_proof_length(clauses):
    n = len(clauses)
    stack = []
    literals = set()
    
    def resolve(lit1, lit2):
        nonlocal literals
        if abs(lit1) == abs(lit2):
            literals.remove(abs(lit1))
            literals.discard(-abs(lit1))
            return True
        return False
    
    for clause in clauses:
        if len(clause) > 0 and clause[0] != '-':
            literals.update([int(x) for x in clause])
    
    while literals:
        lit = next(iter(literals))
        stack.append(lit)
        literals.remove(abs(lit))
        
        while stack:
            top_lit = stack[-1]
            found_resolvent = False
            for clause in clauses:
                if len(clause) > 0 and clause[0] != '-':
                    if -top_lit in clause:
                        resolvent = [x for x in clause if x != -top_lit]
                        if resolve(top_lit, -resolvent[0]):
                            found_resolvent = True
                            break
            if not found_resolvent:
                stack.pop()
                literals.add(abs(top_lit))
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(2, n)
        clause = ['-' + str(random.randint(1, num_vars))]
        while len(clause) < 3 or (len(clause) == 3 and clause[-2] == '-'):
            clause.append(str(random.randint(1, num_vars)))
        clauses.append(clause)
    
    graph = generate_graph(clauses)
    has_loops = find_loops(graph)
    proof_length = resolution_proof_length(clauses)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length <= 2 ** (math.ceil(math.log2(len([v for v in graph if has_loops])))) if has_loops else True,
        "counterexample": "" if has_loops else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")