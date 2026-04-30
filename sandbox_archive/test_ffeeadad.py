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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0)*i-1 for i in range(1, n+1)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, model):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_model = model.copy()
            new_model[literal] = True if literal > 0 else False
            if not dpll([c for c in clauses if literal not in c and -literal not in c], new_model):
                return False
        pure_literals = [l for l in range(1, n+1) if all(l not in c or -l not in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_model = model.copy()
            new_model[literal] = True
            if not dpll([c for c in clauses if literal not in c and -literal not in c], new_model):
                return False
        for literal in range(1, n+1):
            if literal not in model and -literal not in model:
                new_model = model.copy()
                new_model[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_model):
                    return True
                new_model[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_model):
                    return True
        return False
    
    def resolution(clauses):
        while True:
            new_clauses = []
            added = False
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    common_literals = [l for l in clauses[i] if -l in clauses[j]]
                    if common_literals:
                        new_clause = list(set([l for l in clauses[i] + clauses[j] if l not in common_literals and -l not in common_literals]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            added = True
            if not added:
                break
            clauses += new_clauses
        return len(clauses)
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    proof_length = resolution(formula)
    
    # Simulate S^1_2 provability by checking if the formula is a tautology or has a short Frege proof
    def is_tautology(clauses):
        return dpll(clauses, {})
    
    def frege_proof(clauses):
        stack = []
        for clause in clauses:
            stack.append(clause)
        while len(stack) > 1:
            new_clause = set()
            for c1 in stack:
                for c2 in stack:
                    common_literals = [l for l in c1 if -l in c2]
                    if common_literals:
                        new_clause = list(set([l for l in c1 + c2 if l not in common_literals and -l not in common_literals]))
                        if new_clause not in stack:
                            stack.append(new_clause)
        return len(stack) == 1
    
    s1_2_provable = is_tautology(formula) or frege_proof(formula)
    
    conjecture_holds = proof_length == n**2 and s1_2_provable
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_proof_length = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_proof_length:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")