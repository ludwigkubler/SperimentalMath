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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [f'-{variables[i-1]}', f'{variables[0]}']
            clauses.append(clause)
        for i in range(2, n+1):
            clause = [f'-{variables[i-1]}', f'{variables[i-2]}']
            clauses.append(clause)
        return variables, clauses
    
    def p_adic_valuation(n, p):
        if n % p == 0:
            return 1 + p_adic_valuation(n // p, p)
        else:
            return 0
    
    def resolution_width(clauses):
        width = 2
        while True:
            new_clauses = []
            for clause in clauses:
                if len(clause) > width:
                    new_clauses.extend([c for c in itertools.combinations(clause, width)])
            if not new_clauses:
                return width
            clauses.extend(new_clauses)
            width += 1
    
    def longest_linear_dependency_chain(variables, clauses):
        n = len(variables)
        graph = {i: set() for i in range(n)}
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    u = int(clause[i][1:]) - 1
                    v = int(clause[j][1:]) - 1
                    graph[u].add(v)
                    graph[v].add(u)
        visited = [False] * n
        def dfs(node):
            if visited[node]:
                return 0
            visited[node] = True
            max_depth = 0
            for neighbor in graph[node]:
                max_depth = max(max_depth, dfs(neighbor))
            return max_depth + 1
        max_chain_length = 0
        for i in range(n):
            max_chain_length = max(max_chain_length, dfs(i))
        return max_chain_length
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    p = 2
    valuation = sum(p_adic_valuation(int(var[1:]), p) for var in variables)
    width = resolution_width(clauses)
    l_phi = longest_linear_dependency_chain(variables, clauses)
    k = 0
    while True:
        if math.log(p**k(width)) == n - l_phi:
            break
        k += 1
    
    metric_value = abs(math.log(p**k(width)) - (n - l_phi))
    conjecture_holds = metric_value <= 0.1 * (n - l_phi)
    counterexample = "" if conjecture_holds else f"p-adic valuation: {valuation}, width: {width}, n-l(φ): {n - l_phi}"
    
    return {
        "metric_name": "log(p^k(w(φ)))",
        "metric_value": math.log(p**k(width)),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - (n - l_phi)) <= 0.1 * (n - l_phi)) / len(results)
    
    if all(abs(r - (n - l_phi)) <= 0.1 * (n - l_phi) for r, n, l_phi in zip(results, [run_trial(seed)["instances_tested"] for seed in seeds], [run_trial(seed)["n_max"] for seed in seeds])):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(abs(r - (n - l_phi)) > 0.1 * (n - l_phi) for r, n, l_phi in zip(results, [run_trial(seed)["instances_tested"] for seed in seeds], [run_trial(seed)["n_max"] for seed in seeds])):
        first_failing_seed = next(i for i, r in enumerate(results) if abs(r - (n - l_phi)) > 0.1 * (n - l_phi))
        print(f"RESULT: FALSIFIED counterexample='p-adic valuation and width do not match' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")