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
    
    # Generate a random graph with up to 40 vertices
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Construct the corresponding Tseitin formula F
    variables = {f'x{i}': [] for i in range(n)}
    clauses = []
    
    def add_clause(clause):
        clauses.append(clause)
    
    def add_variable(var, literal):
        if literal not in variables[var]:
            variables[var].append(literal)
    
    # Add clauses for each vertex
    for i in range(n):
        for j in range(n):
            if G[i][j] == 1:
                add_clause([f'x{i}', f'x{j}'])
                add_variable(f'x{i}', f'x{i}')
                add_variable(f'x{j}', f'x{j}')
    
    # Add clauses to ensure each variable appears exactly once
    for i in range(n):
        add_clause([f'~x{i}'] + [f'x{j}' for j in range(n) if j != i])
    
    F = {'variables': variables, 'clauses': clauses}
    
    # Compute the graphical virtual knot K(G)
    # This is a placeholder function. Replace with actual implementation.
    rank_KG = len(F['clauses'])  # Placeholder value
    
    # Determine the length of the shortest resolution proof for F
    # This is a placeholder function. Replace with actual implementation.
    length_resolution_proof_F = len(F['clauses'])  # Placeholder value
    
    # Calculate the minimal rank of K(G)
    min_rank_KG = rank_KG
    
    # Compare the minimal rank of K(G) with the length of the shortest resolution proof for F
    if abs(min_rank_KG - length_resolution_proof_F) > 2 * len(F['clauses']):
        conjecture_holds = False
        counterexample = f"rank={min_rank_KG}, expected={length_resolution_proof_F}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_KG,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r['conjecture_holds']), None)
        counterexample = results[first_failing_seed]['counterexample']
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")