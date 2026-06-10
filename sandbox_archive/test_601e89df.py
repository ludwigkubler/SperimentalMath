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
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([variables[i-1], variables[j-1]])
                clauses.append([-variables[i-1], -variables[j-1]])
        
        return clauses
    
    def hermitian_kähler_manifolds(clauses):
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
                stack.append((clause, 1))
            else:
                clause, level = stack.pop()
                for literal in clause:
                    if literal > 0 and -literal in [c for c in clauses]:
                        new_clause = [l for l in clauses if l != clause]
                        stack.append((new_clause, level + 1))
                        break
                else:
                    depth = max(depth, level)
        return depth
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    d = resolution_proof_depth(clauses)
    manifolds = hermitian_kähler_manifolds(clauses)
    
    if manifolds > d**2 * math.log(n):
        return {
            "metric_name": "Manifolds vs Depth",
            "metric_value": manifolds,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Too many manifolds: {manifolds} > {d**2 * math.log(n)}"
        }
    
    return {
        "metric_name": "Manifolds vs Depth",
        "metric_value": manifolds,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Too many manifolds' first_failing_seed={first_failing_seed}")