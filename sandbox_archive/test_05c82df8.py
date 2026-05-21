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
        # Generate a random Tseitin formula with n variables and clauses
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
        return variables, clauses
    
    def generate_quiver_path(variables, clauses):
        # Generate a quiver path based on the Tseitin formula
        quiver = {}
        for var in variables:
            quiver[var] = []
        for clause in clauses:
            if '-' not in clause:
                u, v = clause.split(' ')
                quiver[u].append(v)
                quiver[v].append(u)
            else:
                u, v = clause[1:].split(' ')
                quiver[u].append(v)
                quiver[v].append(u)
        return quiver
    
    def min_generators(quiver):
        # Find the minimal number of generators for the quiver path
        visited = set()
        generators = []
        
        def dfs(node, parent=None):
            if node not in visited:
                visited.add(node)
                generators.append(node)
                for neighbor in quiver[node]:
                    if neighbor != parent:
                        dfs(neighbor, node)
        
        for node in quiver:
            if node not in visited:
                dfs(node)
        
        return len(generators)
    
    def resolution_length(variables, clauses):
        # Simulate the resolution proof length
        stack = []
        while stack or clauses:
            if not stack:
                clause = random.choice(clauses)
                variables.remove(clause[1:])
                clauses.remove(clause)
            else:
                top = stack.pop()
                if top in clauses:
                    clauses.remove(top)
                elif '-' + top in clauses:
                    clauses.remove('-' + top)
                else:
                    stack.append(top)
        return len(stack)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    quiver = generate_quiver_path(variables, clauses)
    min_gen = min_generators(quiver)
    proof_length = resolution_length(variables, clauses)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2 ** (min_gen + math.log(n, 2)),
        "counterexample": "" if proof_length >= 2 ** (min_gen + math.log(n, 2)) else f"n={n}, min_gen={min_gen}, proof_length={proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break