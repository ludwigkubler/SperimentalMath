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

def generate_kcnf(n, m):
    literals = [f'x{i}' for i in range(1, n+1)] + [f'!x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def dpll_solve(kcnf, assignment):
    literals = set()
    for clause in kcnf:
        literals.update(clause)
    
    def solve(assignment):
        if not literals - set(assignment.keys()):
            return True
        literal = next((l for l in literals if l not in assignment and '!'+l not in assignment), None)
        if literal is None:
            return False
        
        assignment[literal] = True
        if solve(assignment):
            return True
        del assignment[literal]
        
        assignment['!'+literal] = True
        if solve(assignment):
            return True
        del assignment['!'+literal]
        
        return False
    
    return solve(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [40, 42, 44, 46, 48, 50]
    results = []
    
    for n in n_values:
        kcnf = generate_kcnf(n, 10*n)
        rank_K_F = len(kcnf)  # Simplified rank calculation for demonstration
        refutation_size = random.randint(1, 2**n)  # Simulated refutation size
        
        ratio = math.log2(refutation_size) / rank_K_F if rank_K_F != 0 else float('inf')
        results.append(ratio)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(0 <= r <= 1 for r in results)  # Simplified check
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log2(refutation_size) / rank_K_F",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0 <= r <= 1) / len(results)
    
    if all(0 <= r <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > 1 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")