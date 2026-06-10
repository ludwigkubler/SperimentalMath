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
        literals = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate clauses for the Tseitin formula
        for i in range(1, n):
            clause = [-literals[i-1], literals[i]]
            clauses.append(clause)
        
        # Add a final clause to ensure the formula is satisfiable
        clause = [literals[-1]] + [-literals[0]]
        clauses.append(clause)
        
        return literals, clauses
    
    def calculate_frege_proof_length(clauses):
        # Simplistic estimation of Frege proof length (for demonstration purposes)
        return len(clauses) * 2
    
    def calculate_minimal_representation_dimension(n):
        # Simplistic estimation of minimal representation dimension (for demonstration purposes)
        return n + 1
    
    literals, clauses = generate_tseitin_formula(40)
    frege_proof_length = calculate_frege_proof_length(clauses)
    dim_V = calculate_minimal_representation_dimension(len(literals))
    
    if frege_proof_length == 0:
        return {
            "metric_name": "Frege Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "Frege proof length is zero"
        }
    
    ratio = dim_V / frege_proof_length
    
    return {
        "metric_name": "Ratio of Dimension to Frege Proof Length",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": abs(ratio - 1) <= 0.1,  # Adjust epsilon as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")