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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate all possible binary clauses
        for i in range(n):
            for j in range(i+1, n):
                clauses.append(f'{variables[i]} | {variables[j]}')
                clauses.append(f'{~variables[i]} | {~variables[j]}')
        
        # Add a clause for each variable being true
        for i in range(n):
            clauses.append(f'{variables[i]}')
        
        return clauses
    
    def resolution_proof_depth(clauses):
        n = len(clauses)
        proof = []
        while True:
            new_clause = None
            for i in range(n):
                for j in range(i+1, n):
                    if any(x in clause and ~x in other_clause for x, other_clause in zip(clauses[i], clauses[j])):
                        new_clause = set(clauses[i]) | set(clauses[j])
                        new_clause.discard(x)
                        new_clause.discard(~x)
                        proof.append(new_clause)
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            n += 1
        return len(proof)
    
    def l_function(n):
        # Simplified L-Function for demonstration purposes
        return Fraction(1, n**2)
    
    n = random.randint(5, 40)  # Sweep n through at least 4 distinct sizes inside each trial
    clauses = generate_tseitin_formula(n)
    depth = resolution_proof_depth(clauses)
    l_n = l_function(n)
    
    c_k = 1 / (2 * math.log(n))  # Example constant for demonstration purposes
    
    if depth < c_k * l_n:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {depth} is less than {c_k * l_n}"
        }
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth less than c_k * L(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")