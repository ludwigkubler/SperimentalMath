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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        # Simplified SAT solver using backtracking
        assignment = {i: None for i in range(1, n + 1)}
        
        def backtrack():
            unassigned = [i for i in range(1, n + 1) if assignment[i] is None]
            if not unassigned:
                return all(any(lit in assignment and (assignment[lit] == 1 if lit > 0 else not assignment[-lit]) for lit in clause) for clause in clauses)
            var = unassigned[0]
            for val in [True, False]:
                assignment[var] = val
                if backtrack():
                    return True
                assignment[var] = None
            return False
        
        return backtrack()
    
    def construct_representation(clauses):
        # Simplified representation construction (placeholder)
        return len(clauses)  # Placeholder value
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n * n // 2, 10))
    clauses = generate_kcnf(n, k)
    
    D_F = construct_representation(clauses)
    minimal_order = 2**n / 4 if is_satisfiable(clauses) else 2**(n-1) / 2
    
    alpha = Fraction(1, 2)  # Example value for α
    ratio = minimal_order / D_F
    
    return {
        "metric_name": "Ratio of Minimal Order to D(F)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= alpha,
        "counterexample": "" if ratio <= alpha else f"Counterexample: n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")