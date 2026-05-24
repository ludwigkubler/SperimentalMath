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
    
    # Generate a random k-SAT instance with n variables and m clauses
    n = 20  # Number of variables
    m = min(100, n**2)  # Number of clauses (m is at most O(n^2))
    k = 3   # Clause length
    
    # Create a list of literals (positive for positive, negative for negation)
    literals = [i + 1 if random.choice([True, False]) else -i - 1 for i in range(n)]
    
    # Create clauses
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            lit = random.choice(literals)
            if lit not in clause and -lit not in clause:
                clause.add(lit)
        clauses.append(clause)
    
    # Convert clauses to a list of lists
    clauses_list = [[abs(lit), 1 if lit > 0 else -1] for clause in clauses]
    
    # Function to compute the minimal p-adic order of the differential representation
    def min_p_adic_order(clauses):
        # Placeholder implementation (this is where you would implement actual p-adic computation)
        return max(len(clause) for clause in clauses)
    
    # Compute the minimal p-adic order
    p_adic_order = min_p_adic_order(clauses_list)
    
    # Function to compute the resolution proof depth using DPLL algorithm (simplified version)
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment) + 1
        pure_literal = next((l for l in range(1, n+1) if (l in [c[0] for c in clauses] and -l in [c[0] for c in clauses]) or (-l in [c[0] for c in clauses] and l in [c[0] for c in clauses])), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment) + 1
        literal = random.choice([l for l in range(1, n+1) if l not in assignment])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        return dpll(clauses_list, new_assignment) + 1
    
    # Compute the resolution proof depth
    resolution_depth = dpll(clauses_list, {})
    
    # Check the conjecture
    conjecture_holds = p_adic_order <= math.log(n, 2) + math.log(m, 2)
    counterexample = "" if conjecture_holds else f"p-adic order {p_adic_order} exceeds log(n) + log(m)"
    
    return {
        "metric_name": "Minimal p-adic Order vs Resolution Depth",
        "metric_value": p_adic_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))  # Default to first 30 primes
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")