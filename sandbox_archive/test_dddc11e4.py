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

def is_tautology(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    assignment = {var: False for var in variables}
    stack = []
    for var in range(1, max(variables) + 1):
        stack.append((var, True))
        stack.append((var, False))
    
    while stack:
        literal, value = stack.pop()
        if literal < 0:
            continue
        if literal not in assignment:
            assignment[literal] = value
        else:
            if assignment[literal] != value:
                return False
    
    for clause in clauses:
        if all(lit not in assignment or assignment[abs(lit)] == (lit > 0) for lit in clause):
            continue
        return False
    
    return True

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()
        value = literal > 0
        assignment[abs(literal)] = value
        
        new_clauses = []
        for clause in clauses:
            if any(lit not in assignment or assignment[abs(lit)] == (lit > 0) for lit in clause):
                continue
            if all(lit not in assignment or assignment[abs(lit)] != (lit > 0) for lit in clause):
                return False
            new_clauses.append([l for l in clause if l != literal and -l not in clause])
        clauses = new_clauses
    
    pure_literals = [l for l, count in Counter(lit for c in clauses for lit in c).items() if count % 2 == 1]
    while pure_literals:
        literal = pure_literals.pop()
        value = literal > 0
        assignment[abs(literal)] = value
        
        new_clauses = []
        for clause in clauses:
            if any(lit not in assignment or assignment[abs(lit)] == (lit > 0) for lit in clause):
                continue
            if all(lit not in assignment or assignment[abs(lit)] != (lit > 0) for lit in clause):
                return False
            new_clauses.append([l for l in clause if l != literal and -l not in clause])
        clauses = new_clauses
    
    if not clauses:
        return True
    
    var = next(var for var, count in Counter(lit for c in clauses for lit in c).items() if count > 0)
    assignment[var] = True
    if dpll(clauses, assignment):
        return True
    assignment.pop(var)
    
    assignment[var] = False
    if dpll(clauses, assignment):
        return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k_values = [1, 2, 3]
    results = []
    
    for k in k_values:
        clauses = []
        for _ in range(3 * n):
            literals = random.sample(range(-n, 0), n) + random.sample(range(1, n + 1), n)
            clause = [literals[i] for i in random.sample(range(n), n // 2)]
            clauses.append(clause)
        
        if is_tautology(clauses):
            proof_length = 0
        else:
            proof_length = dpll(clauses)
        
        results.append({
            "n": n,
            "k": k,
            "proof_length": proof_length,
            "tautology": is_tautology(clauses)
        })
    
    total_proofs = sum(result["proof_length"] for result in results if result["tautology"])
    avg_proof_length = total_proofs / len(results)
    std_dev = math.sqrt(sum((result["proof_length"] - avg_proof_length) ** 2 for result in results if result["tautology"]) / len(results))
    
    conjecture_holds = all(result["proof_length"] == n**k for result in results if result["tautology"])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_proof_length",
        "metric_value": avg_proof_length,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_proof_length = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_proof_length) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_proof_length} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")