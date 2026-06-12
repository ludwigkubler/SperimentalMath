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
    
    def resolution_proof_tree(clauses):
        # Convert clauses to a set for efficient lookup and removal
        clauses = set(tuple(c) for c in clauses)
        proof = []
        
        while len(clauses) > 1:
            clause1, clause2 = random.sample(list(clauses), 2)
            new_clauses = set()
            for literal in clause1:
                if literal not in clause2 and -literal not in clause2:
                    new_clause = tuple(sorted([l for l in clause1 + clause2 if l != literal and -l != literal]))
                    new_clauses.add(new_clause)
            proof.append((clause1, clause2, new_clauses))
            clauses.update(new_clauses)
        
        return proof, clauses
    
    def topological_entropy(proof):
        n = len(proof)
        entropy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(l in proof[j] or -l in proof[j] for l in proof[i]):
                    entropy += math.log2(1 / (j - i))
        return entropy
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Clause: x1 ∨ ¬x2
        clauses.append([variables[0], -variables[1]])
        
        # Clause: ¬x1 ∨ x3
        clauses.append([-variables[0], variables[2]])
        
        # Clause: x2 ∨ ¬x4
        clauses.append([variables[1], -variables[3]])
        
        return clauses
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = tseitin_formula(n)
    
    proof, _ = resolution_proof_tree(clauses)
    entropy = topological_entropy(proof)
    
    metric_value = entropy / (n * math.log2(n))
    instances_tested = 1
    n_max = n
    conjecture_holds = abs(metric_value - 1) <= 3
    counterexample = "" if conjecture_holds else f"Entropy {entropy} not within O(n log n)"
    
    return {
        "metric_name": "Topological Entropy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")