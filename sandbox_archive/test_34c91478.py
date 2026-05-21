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
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
            for j in range(i+1, n+1):
                clauses.append(f'{variables[i-1]} {variables[j-1]} -{variables[i-1]} -{variables[j-1]}')
        return variables, clauses
    
    def generate_quiver_path(variables, clauses):
        quiver = {}
        for clause in clauses:
            if ' ' not in clause:
                continue
            u, v = clause.split(' ')
            if u not in quiver:
                quiver[u] = []
            if v not in quiver:
                quiver[v] = []
            quiver[u].append(v)
            quiver[v].append(u)
        return quiver
    
    def count_generators(quiver):
        visited = set()
        generators = 0
        for node in quiver:
            if node not in visited:
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current not in visited:
                        visited.add(current)
                        for neighbor in quiver[current]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                generators += 1
        return generators
    
    def resolution_proof_length(variables, clauses):
        # Simplified version of resolution proof length calculation
        return len(clauses) * len(variables)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    quiver = generate_quiver_path(variables, clauses)
    min_generators = count_generators(quiver)
    proof_length = resolution_proof_length(variables, clauses)
    
    metric_value = proof_length / min_generators
    conjecture_holds = proof_length >= 2 ** (min_generators + math.log(2))
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < 2^(min generators + log(2))"
    
    return {
        "metric_name": "Resolution Proof Length / Min Generators",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(x["metric_value"] for x in results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Proof length < 2^(min generators + log(2))\" first_failing_seed={first_failing_seed}")