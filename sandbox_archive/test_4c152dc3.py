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
    
    def generate_tseitin_formula(n):
        vertices = list(range(1, n+1))
        literals = [f'x{i}' for i in vertices]
        clauses = []
        
        # Create clauses for each vertex
        for v in vertices:
            clauses.append([literals[v-1]])
            clauses.append([-literals[v-1]])
        
        # Create clauses for edges
        for u, v in random.sample(list(itertools.combinations(vertices, 2)), n-1):
            literals_u = [f'x{i}' if i != u else f'-x{i}' for i in vertices]
            literals_v = [f'x{i}' if i != v else f'-x{i}' for i in vertices]
            clauses.append([literals_u[v-1], literals_v[u-1]])
        
        # Create a clause to ensure at least one vertex is true
        clauses.append([f'-x{i}' for i in vertices])
        
        formula = ' & '.join(f'({c})' for c in clauses)
        return formula, literals
    
    def dpll(formula, assignment):
        if not formula:
            return True
        clause = next(c for c in formula.split(' & ') if any(l in assignment and assignment[l] == 1 for l in c.split(' | ')))
        literal = next(l for l in clause.split(' | ') if l[0] != '-')
        if literal in assignment:
            if assignment[literal]:
                return dpll(formula.replace(f'({literal} | {l})', '').replace(f'({-literal} | {l})', ''), assignment)
            else:
                return dpll(formula.replace(f'({literal} | {l})', '').replace(f'({-literal} | {l})', ''), {**assignment, literal: 1})
        else:
            if dpll(formula.replace(f'({literal} | {l})', '').replace(f'({-literal} | {l})', ''), {**assignment, literal: 0}):
                return True
            elif dpll(formula.replace(f'({literal} | {l})', '').replace(f'({-literal} | {l})', ''), {**assignment, literal: 1}):
                return True
            else:
                return False
    
    def resolution_length(formula):
        clauses = formula.split(' & ')
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    c1, c2 = clauses[i], clauses[j]
                    literals = set(c1.split(' | ')) & set(c2.split(' | '))
                    if literals:
                        new_clause = [l for l in c1.split(' | ') if l not in literals] + [l for l in c2.split(' | ') if l not in literals]
                        new_clauses.append(' | '.join(new_clause))
            if len(new_clauses) == len(clauses):
                break
            clauses = new_clauses
        return len(clauses)
    
    def min_nonnegative_minor_invariant(n):
        graph = {i: set() for i in range(1, n+1)}
        edges = random.sample(list(itertools.combinations(range(1, n+1), 2)), n-1)
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        min_degree = float('inf')
        for i in range(n):
            visited = set()
            dfs(i+1, visited)
            degree = len(graph[i+1])
            if degree < min_degree:
                min_degree = degree
        
        return min_degree
    
    n = random.randint(5, 40)
    formula, literals = generate_tseitin_formula(n)
    resolution_len = resolution_length(formula)
    nu_G = min_nonnegative_minor_invariant(n)
    
    metric_name = "Resolution Length"
    metric_value = resolution_len
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if nu_G > 0:
        correlation = (resolution_len - math.log2(2**nu_G)) / math.sqrt(nu_G)
        if correlation > 0.7:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "Correlation between ν(G) and log2(resolution refutation size of F) did not meet the threshold."
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")