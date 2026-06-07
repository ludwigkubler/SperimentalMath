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
    
    def generate_instance(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        literals = {}
        count = 0
        formula = []
        for i, clause in enumerate(clauses):
            literal = f"p{i+1}"
            literals[literal] = count
            count += 1
            formula.append([literal])
            for lit in clause:
                neg_lit = f"-{lit}"
                if neg_lit not in literals:
                    literals[neg_lit] = count
                    count += 1
                formula.append([neg_lit, literal])
        return formula, literals
    
    def resolution_width(formula):
        clauses = [set(clause) for clause in formula]
        queue = list(clauses)
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 0:
                continue
            for clause2 in queue:
                if len(clause2) == 0:
                    continue
                for lit in clause1:
                    neg_lit = f"-{lit}"
                    if neg_lit in clause2:
                        new_clause = clause2 - {neg_lit} | (clause1 - {lit})
                        if len(new_clause) == 0:
                            return float('inf')
                        queue.append(list(new_clause))
        return max(len(clause) for clause in clauses)
    
    def local_chromatic_number(graph):
        n = len(graph)
        colors = [-1] * n
        color_count = [0] * (n + 1)
        
        def is_safe(v, c):
            for i in range(n):
                if graph[v][i] and colors[i] == c:
                    return False
            return True
        
        def backtrack(v):
            if v == n:
                return True
            for c in range(1, n + 1):
                if is_safe(v, c):
                    colors[v] = c
                    color_count[c] += 1
                    if backtrack(v + 1):
                        return True
                    colors[v] = -1
                    color_count[c] -= 1
            return False
        
        backtrack(0)
        return max(color_count)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    instance = generate_instance(n, m)
    formula, literals = tseitin_formula(instance)
    width = resolution_width(formula)
    
    graph = [[False] * n for _ in range(n)]
    for clause in instance:
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != lit2:
                    i1 = abs(lit1) - 1
                    i2 = abs(lit2) - 1
                    graph[i1][i2] = True
                    graph[i2][i1] = True
    
    chromatic_number = local_chromatic_number(graph)
    
    return {
        "metric_name": "local_chromatic_number",
        "metric_value": abs(chromatic_number - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(chromatic_number - width) <= 5,  # Assuming k=5 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")