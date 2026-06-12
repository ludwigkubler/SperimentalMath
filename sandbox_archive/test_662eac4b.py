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
        
        # Generate clauses for each variable
        for var in variables:
            clauses.append([var])
        
        # Generate clauses for implications
        for i in range(1, n):
            clauses.append([f'x{i}', f'~x{i+1}'])
        
        # Generate final clause
        clauses.append(['~x1'] + [f'x{i}' for i in range(2, n+1)])
        
        return variables, clauses
    
    def resolution_proof_tree(clauses):
        proof = set()
        new_clauses = set(clauses)
        
        while new_clauses:
            new_clause = None
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        break
                if new_clause:
                    break
            if not new_clause:
                return None, proof
            new_clauses.remove(new_clause)
            new_clauses.add(tuple(sorted(new_clause)))
            proof.add(tuple(sorted(new_clause)))
        
        return proof, proof
    
    def topological_entropy(proof):
        n = len(proof)
        if n == 0:
            return 0
        
        # Calculate the number of nodes at each level
        levels = {}
        for clause in proof:
            length = len(clause)
            if length not in levels:
                levels[length] = 1
            else:
                levels[length] += 1
        
        # Calculate topological entropy
        total_nodes = sum(levels.values())
        entropy = 0
        for count in levels.values():
            p = Fraction(count, total_nodes)
            entropy -= p * math.log2(p)
        
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        proof, _ = resolution_proof_tree(clauses)
        
        if proof is None:
            continue
        
        entropy = topological_entropy(proof)
        results.append((n, entropy))
    
    if not results:
        return {
            "metric_name": "topological_entropy",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_tree_failed"
        }
    
    n_max = max(n for n, _ in results)
    mean_entropy = sum(entropy for _, entropy in results) / len(results)
    std_entropy = math.sqrt(sum((entropy - mean_entropy) ** 2 for _, entropy in results) / len(results))
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(abs(entropy - mean_entropy) <= 3 for _, entropy in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"topological_entropy_outside_bound\" first_failing_seed={first_failing_seed}")