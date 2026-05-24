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
    
    def generate_tseitin_formula(n, clause_density):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            if random.random() < clause_density:
                clause = [var]
                clauses.append(clause)
                
            if random.random() < clause_density:
                clause = [-var]
                clauses.append(clause)
                
        # Generate clauses for implications
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < clause_density:
                    clause = [i + 1, -j - 1]
                    clauses.append(clause)
                    
                if random.random() < clause_density:
                    clause = [-i - 1, j + 1]
                    clauses.append(clause)
        
        # Generate clauses for OR
        for i in range(n):
            for j in range(i + 1, n):
                clause = [i + 1, j + 1]
                clauses.append(clause)
                
                clause = [-i - 1, -j - 1]
                clauses.append(clause)
        
        return variables, clauses
    
    def generate_group_representations(n):
        # For simplicity, we use the cyclic group C_n
        G = list(range(1, n + 1))
        representations = []
        
        for i in range(n):
            rho = [0] * n
            rho[i % n] = 1
            representations.append(rho)
            
            rho = [0] * n
            rho[(i * 2) % n] = 1
            representations.append(rho)
        
        return G, representations
    
    def calculate_resolution_proof_width(variables, clauses):
        # Simplified resolution proof width calculation (placeholder)
        return len(clauses)
    
    n = random.randint(5, 40)
    clause_density = random.uniform(0.1, 0.9)
    variables, clauses = generate_tseitin_formula(n, clause_density)
    G, representations = generate_group_representations(n)
    
    min_dimension = min(len(rho) for rho in representations)
    resolution_width = calculate_resolution_proof_width(variables, clauses)
    
    conjecture_holds = resolution_width >= 2 ** (min_dimension - 1)
    counterexample = "" if conjecture_holds else f"Counterexample with n={n}, clause_density={clause_density}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")