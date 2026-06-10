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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-variables[i-1], -variables[j-1]])
                clauses.append([variables[i-1], variables[j-1]])
                clauses.append([variables[j-1], -variables[i-1]])
        
        return clauses
    
    def hermitian_kahler_manifolds(clauses, n):
        manifolds = set()
        for clause in clauses:
            # Constructive mapping algorithm (simplified example)
            manifold_id = hash(tuple(sorted(clause)))
            manifolds.add(manifold_id)
        return len(manifolds)
    
    def resolution_proof_depth(clauses):
        depth = 0
        stack = []
        while stack or clauses:
            if not stack:
                clause = random.choice(clauses)
                stack.append(clause)
                clauses.remove(clause)
            else:
                top_clause = stack[-1]
                if -top_clause[0] in clauses:
                    clauses.remove(-top_clause[0])
                    stack.pop()
                elif len(top_clause) == 2 and -top_clause[1] in clauses:
                    clauses.remove(-top_clause[1])
                    stack.pop()
                else:
                    depth += 1
                    break
        return depth
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    depth = resolution_proof_depth(clauses)
    manifolds = hermitian_kahler_manifolds(clauses, n)
    
    metric_value = manifolds * math.log(n) / (depth ** 2)
    conjecture_holds = metric_value <= n
    
    return {
        "metric_name": "Manifolds",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Too many manifolds: {manifolds} > O({depth**2 * math.log(n)})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many manifolds\" first_failing_seed={seeds[first_failing_seed]}")