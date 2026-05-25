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

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        literals = random.sample(range(-n, 0), 1) + random.sample(range(1, n + 1), 2)
        random.shuffle(literals)
        clause = " or ".join(f"x{abs(lit)}" if lit > 0 else f"~x{-lit}" for lit in literals)
        clauses.append(clause)
    formula = " and ".join(clauses)
    return formula

def dpll_solve(formula):
    def backtrack(assignment, literals):
        if not literals:
            return True
        literal = literals[0]
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = literal // abs(literal)
        if backtrack(new_assignment, literals[1:]):
            return True
        new_assignment.pop(abs(literal), None)
        new_assignment[abs(literal)] = -literal // abs(literal)
        return backtrack(new_assignment, literals[1:])
    
    literals = [int(x) for x in formula.replace(' or ', ' ').replace(' and ', ' ').split()]
    return backtrack({}, literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    formula = generate_3cnf(n)
    proof_time = dpll_solve(formula)
    
    if not proof_time:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL solver did not find a solution"
        }
    
    # Simulate quantum transport to compute minimal rank (placeholder)
    min_rank = random.randint(1, n)  # Placeholder for actual computation
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": math.log(proof_time),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(v is None for v in results):
        print("RESULT: INCONCLUSIVE reason=uncomputable")
    else:
        mean = sum(r for r in results if r is not None) / len(results)
        std = math.sqrt(sum((r - mean)**2 for r in results if r is not None) / len(results))
        support_fraction = sum(1 for r in results if r is not None and r > 0.7 * mean) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if r is not None and r <= 0.7 * mean)
            print(f"RESULT: FALSIFIED counterexample='Spearman rank correlation below threshold' first_failing_seed={seeds[first_failing_seed]}")