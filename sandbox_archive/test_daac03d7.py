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

def generate_cnf(n):
    clauses = []
    for _ in range(n * (n + 1) // 2):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    for literal in cnf[0]:
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if not any(l in c or -l in c for l in new_assignment)], new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        proof_length = len(dpll(cnf))
        unitary_group_order = n * (n + 1) // 2
        O_phi = math.sqrt(proof_length ** 2)
        
        results.append({
            "n": n,
            "proof_length": proof_length,
            "unitary_group_order": unitary_group_order,
            "O_phi": O_phi
        })
    
    correlation_coefficient = sum((r["unitary_group_order"] - sum(r["unitary_group_order"] for r in results) / len(results)) * (r["O_phi"] - sum(r["O_phi"] for r in results) / len(results)) for r in results) / ((len(results) - 1) * math.sqrt(sum((r["unitary_group_order"] - sum(r["unitary_group_order"] for r in results) / len(results)) ** 2 for r in results)) * math.sqrt(sum((r["O_phi"] - sum(r["O_phi"] for r in results) / len(results)) ** 2 for r in results)))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "correlation_coefficient < 0.8" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] == "correlation_coefficient < 0.8")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")