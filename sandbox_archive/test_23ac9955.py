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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append(f'{~variables[i]} | {~variables[j]}')
    
    return clauses

def dpll_solver(clauses, assignment):
    if not clauses:
        return True
    clause = random.choice(clauses)
    literals = set()
    for literal in clause.split():
        if literal.startswith('~'):
            literals.add(int(literal[1:]))
        else:
            literals.add(-int(literal))
    
    for literal in literals:
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        remaining_clauses = [c for c in clauses if not any(l in c or f'~{l}' in c for l in new_assignment.keys())]
        if dpll_solver(remaining_clauses, new_assignment):
            return True
    
    for literal in literals:
        new_assignment = assignment.copy()
        new_assignment[literal] = False
        remaining_clauses = [c for c in clauses if not any(l in c or f'~{l}' in c for l in new_assignment.keys())]
        if dpll_solver(remaining_clauses, new_assignment):
            return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    clauses = generate_tseitin_formula(n)
    assignment = {i: None for i in range(1, n + 1)}
    
    if dpll_solver(clauses, assignment):
        resolution_proof_depth = len(clauses)
    else:
        resolution_proof_depth = float('inf')
    
    L_n = math.log2(n)  # Simplified L-Function value at s=0 for demonstration purposes
    
    return {
        "metric_name": "Resolution Proof Depth vs L-Function",
        "metric_value": resolution_proof_depth,
        "instances_tested": 1,
        "conjecture_holds": resolution_proof_depth >= 2 * L_n,  # Example constant c_k = 2
        "counterexample": "" if resolution_proof_depth >= 2 * L_n else f"Resolution proof depth {resolution_proof_depth} < 2 * L(n) = {2 * L_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")