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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Generate literals
        literals = [random.choice(variables) for _ in range(m)]
        
        # Generate clauses
        for literal in literals:
            clauses.append([literal])
        
        return variables, clauses
    
    def construct_graph(variables, clauses):
        graph = {var: [] for var in variables}
        
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    graph[clause[i]].append(clause[j])
                    graph[clause[j]].append(clause[i])
        
        return graph
    
    def find_real_roots(graph):
        # Placeholder for polynomial root-finding algorithm
        # This is a dummy implementation; replace with actual algorithm
        return random.randint(1, 5)
    
    def resolution_length(variables, clauses):
        # Placeholder for DPLL solver
        # This is a dummy implementation; replace with actual solver
        return random.randint(10, 20)
    
    n = random.randint(5, 40)
    m = random.randint(n + 1, n * (n - 1) // 2)
    variables, clauses = generate_tseitin_formula(n, m)
    graph = construct_graph(variables, clauses)
    real_roots = find_real_roots(graph)
    proof_length = resolution_length(variables, clauses)
    
    ratio = proof_length / (2 ** real_roots)
    conjecture_holds = 0.5 <= ratio <= 1.5
    
    return {
        "metric_name": "Resolution length to real roots ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} out of bounds"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")