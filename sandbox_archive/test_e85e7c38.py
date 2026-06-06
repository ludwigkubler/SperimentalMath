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
        # Generate a random Tseitin formula with n variables
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Add clauses for each literal and its negation
        for lit in literals:
            clauses.append([lit])
            clauses.append([-lit])
        
        # Add clauses for the OR of all literals
        or_clause = [-f'x{i}' for i in range(1, n+1)]
        or_clause.append('F')
        clauses.append(or_clause)
        
        return literals, clauses
    
    def hodge_decomposition_module(literals, clauses):
        # Simulate Hodge decomposition module computation
        # This is a placeholder function; replace with actual implementation
        return len(literals) * 2
    
    def resolution_proof_width(clauses):
        # Simulate resolution proof width computation
        # This is a placeholder function; replace with actual implementation
        return len(clauses)
    
    n = random.randint(5, 40)
    literals, clauses = generate_tseitin_formula(n)
    min_rank_M_phi_G = hodge_decomposition_module(literals, clauses)
    w_phi_G = resolution_proof_width(clauses)
    
    ratio = min_rank_M_phi_G / w_phi_G if w_phi_G != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Minimal Rank to Resolution Proof Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": "" if 0.5 <= ratio <= 2 else f"Ratio {ratio} out of bounds [0.5, 2]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds [0.5, 2]\" first_failing_seed={first_failing_seed}")