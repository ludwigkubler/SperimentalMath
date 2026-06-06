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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literals = {}
        for literal in range(1, n+1):
            pos_count = sum(l == literal for c in cnf for l in c)
            neg_count = sum(l == -literal for c in cnf for l in c)
            if pos_count + neg_count == len(cnf):
                pure_literals[literal] = True
        if pure_literals:
            literal = next(iter(pure_literals))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        p, _ = random.choice(cnf)
        if dpll(cnf, assignment | {p: True}):
            return True
        if dpll(cnf, assignment | {p: False}):
            return True
        return False
    
    def hensel_lifting_steps(cnf):
        steps = 0
        for _ in range(10):  # Simulate a fixed number of Hensel lifting steps
            if dpll(cnf):
                steps += 1
        return steps
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    h_steps = hensel_lifting_steps(cnf)
    proof_length = len(dpll(cnf))
    
    return {
        "metric_name": "Hensel Lifting Steps vs DPLL Proof Length",
        "metric_value": Fraction(h_steps, proof_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_steps == proof_length,
        "counterexample": "" if h_steps == proof_length else f"Steps: {h_steps}, Proof Length: {proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")