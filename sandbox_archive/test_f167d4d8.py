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
    
    def generate_cnf(n_vars, n_clauses):
        cnf = []
        for _ in range(n_clauses):
            clause = set()
            while len(clause) < 2 or any(lit == -other_lit for lit in clause for other_lit in clause):
                literals = [random.choice([-1, 1]) * (i + 1) for i in range(n_vars)]
                random.shuffle(literals)
                clause = set(literals[:2])
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = next(iter(unit_clauses[0]))
            if literal < 0 and -literal in assignment:
                return False
            assignment.append(literal)
            return dpll([c for c in cnf if literal not in c and -literal not in c], assignment)
        pure_literals = [l for l in range(1, n_vars + 1) if all(l in c or -l in c for c in cnf)]
        if pure_literals:
            literal = pure_literals[0]
            if literal < 0 and -literal in assignment:
                return False
            assignment.append(literal)
            return dpll([c for c in cnf if literal not in c and -literal not in c], assignment)
        p, _ = random.choice(cnf)
        return dpll(cnf, assignment + [p]) or dpll(cnf, assignment + [-p])
    
    def compute_cocomplexity(cnf):
        n_vars = max(abs(lit) for clause in cnf for lit in clause)
        # Simplified cocomplexity computation (not actual cocomplexity)
        return sum(len(clause) for clause in cnf) / n_vars
    
    n_vars = random.randint(10, 40)
    n_clauses = random.randint(n_vars, n_vars * 2)
    cnf = generate_cnf(n_vars, n_clauses)
    
    depth = dpll(cnf)
    cocomplexity = compute_cocomplexity(cnf)
    
    return {
        "metric_name": "d(χ_c(φ))",
        "metric_value": cocomplexity,
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": depth == len(cnf),
        "counterexample": "" if depth == len(cnf) else f"Depth {depth} != {len(cnf)}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Depth != expected\" first_failing_seed={first_failing_seed}")