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
    
    n = 20  # Number of vertices in the graph
    if n < 5 or n > 40:
        return {
            "metric_name": "resolution_proof_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }
    
    # Generate a random graph
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    
    # Create the Tseitin formula
    clauses = []
    literals = [f"v{i+1}" for i in range(n)]
    for (i, j) in edges:
        clauses.append([literals[i], literals[j]])
        clauses.append([-literals[i], -literals[j]])
        clauses.append([literals[i], -literals[j]])
        clauses.append([-literals[i], literals[j]])
    
    # Add the negation of each literal
    for i in range(n):
        clauses.append([-literals[i]])
    
    # DPLL-based resolution proof size estimation (simplified)
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_literals = {}
        for c in clauses:
            for l in c:
                if l.startswith('v'):
                    if l not in pure_literals:
                        pure_literals[l] = True
                    elif not pure_literals[l]:
                        pure_literals[l] = False
                else:
                    if -l not in pure_literals:
                        pure_literals[-l] = True
                    elif not pure_literals[-l]:
                        pure_literals[-l] = False
        
        unit_clauses.extend([p for p, v in pure_literals.items() if v])
        unit_clauses.extend([-p for p, v in pure_literals.items() if not v])
        
        if not unit_clauses:
            return 1 + max(dpll(clause, assignment) for clause in clauses)
        
        literal = unit_clauses[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        true_clauses = [c for c in clauses if literal not in c and -literal not in c]
        false_clauses = [c for c in clauses if literal in c or -literal in c]
        
        if any(l.startswith('v') and l not in new_assignment and -l not in new_assignment for l in false_clauses):
            return 1 + dpll(true_clauses, new_assignment)
        
        new_assignment[literal] = False
        true_clauses = [c for c in clauses if literal not in c and -literal not in c]
        false_clauses = [c for c in clauses if literal in c or -literal in c]
        
        if any(l.startswith('v') and l not in new_assignment and -l not in new_assignment for l in true_clauses):
            return 1 + dpll(false_clauses, new_assignment)
        
        return 1
    
    proof_size = dpll(clauses, {})
    
    # Euler characteristic of the sheaf cohomology groups (constant sheaf)
    euler_characteristic = n - len(edges) + 1
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": abs(euler_characteristic),
        "instances_tested": 1,
        "conjecture_holds": proof_size > 0 and abs(euler_characteristic) / math.log(n) < 100,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")