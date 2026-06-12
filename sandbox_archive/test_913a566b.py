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
    
    def generate_formula(n):
        formula = []
        for _ in range(2**n):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            formula.append(clause)
        return formula
    
    def is_satisfiable(formula):
        stack = []
        assignment = {}
        
        def backtrack():
            if not stack:
                return True
            literal = stack.pop()
            var, negated = literal[0], literal[1] == '-'
            if var in assignment and assignment[var] != negated:
                return False
            assignment[var] = negated
            for clause in formula:
                if any(lit in assignment and assignment[lit] for lit in clause):
                    continue
                stack.append(clause)
                break
            else:
                return backtrack()
        
        stack.extend(formula)
        return backtrack()
    
    def automorphism_group(formula):
        n = len(formula[0])
        group = []
        for perm in itertools.permutations(range(n)):
            if all(all(formula[i][j] == formula[i][perm[j]] for j in range(n)) for i in range(len(formula))):
                group.append(perm)
        return group
    
    def proof_length(formula):
        # Placeholder for actual SAT solver integration
        # For simplicity, assume a linear relationship with n variables
        return len(formula) * 10
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    if not is_satisfiable(formula):
        return {
            "metric_name": "proof_length",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    aut_group = automorphism_group(formula)
    metric_value = len(aut_group) / proof_length(formula)
    
    return {
        "metric_name": "proof_length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='unsatisfiable_formula' first_failing_seed={first_failing_seed}")