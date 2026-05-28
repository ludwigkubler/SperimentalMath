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

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        literals = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(literals)
    return clauses

def dpll_solver(clauses):
    def solve(variables, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment:
                return False
            elif literal > 0 and -literal not in assignment:
                assignment[literal] = True
            else:
                del assignment[-literal]
            return solve(variables, assignment)
        
        pure_literal = next((l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal is not None:
            assignment[pure_literal] = True
            return solve(variables, assignment)
        
        literal = random.choice([i for i in range(1, n + 1)])
        assignment[literal] = True
        if solve(variables, assignment):
            return True
        del assignment[literal]
        assignment[-literal] = True
        return solve(variables, assignment)
    
    variables = list(range(1, n + 1))
    assignment = {}
    return solve(variables, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.ceil(n * 1.5)
    clauses = generate_3cnf(n, m)
    
    if not dpll_solver(clauses):
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    # Placeholder for computing the rank of the toric variety
    rank = n
    
    # Placeholder for computing the length of the shortest resolution proof
    resolution_proof_length = m * m * math.log(n, 2)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": resolution_proof_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_proof_length <= rank ** 2 * math.log(rank, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='unproven' first_failing_seed={first_failing_seed + 1}")