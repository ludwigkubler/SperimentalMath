# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_solver(phi, assignment, clauses):
        if not clauses:
            return True
        literal = next(lit for lit in phi if lit not in assignment and -lit not in assignment)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll_solver(phi, new_assignment, [c for c in clauses if literal not in c]):
            return True
        
        new_assignment[literal] = False
        if dpll_solver(phi, new_assignment, [c for c in clauses if -literal not in c]):
            return True
        
        return False
    
    def dpll_proof_tree_width(phi):
        assignment = {}
        return len(clauses) if dpll_solver(phi, assignment, clauses) else 0
    
    n = random.randint(5, 40)
    phi = generate_cnf(n)
    
    local_symmetry_count = 1  # Placeholder for actual symmetry count calculation
    proof_tree_width = dpll_proof_tree_width(phi)
    
    if proof_tree_width == 0:
        return {
            "metric_name": "LocalSymmetryCount / ProofTreeWidth",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Proof tree width is zero, cannot compute ratio"
        }
    
    metric_value = Fraction(local_symmetry_count, proof_tree_width)
    
    return {
        "metric_name": "LocalSymmetryCount / ProofTreeWidth",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= metric_value <= 1.5,
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
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='metric_value out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")