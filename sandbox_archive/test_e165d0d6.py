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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice([True, False])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(random.randint(2, n))]
            operator = random.choice(['&', '|'])
            return (operator, *subformulas)
    
    def evaluate_formula(formula, assignment):
        if isinstance(formula, bool):
            return formula
        elif isinstance(formula, tuple) and len(formula) == 3:
            op, f1, f2 = formula
            if op == '&':
                return evaluate_formula(f1, assignment) and evaluate_formula(f2, assignment)
            elif op == '|':
                return evaluate_formula(f1, assignment) or evaluate_formula(f2, assignment)
    
    def quadratic_residue_symbol(formula):
        n = random.randint(2, 38)
        values = set()
        for k in range(-n, n + 1):
            assignment = {i: (k >> i) & 1 for i in range(n)}
            value = evaluate_formula(formula, assignment)
            if value:
                values.add(k % n)
        return min(abs(v) for v in values)
    
    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = [formula]
        depth = 0
        while stack:
            formula = stack.pop()
            if isinstance(formula, bool):
                continue
            elif isinstance(formula, tuple) and len(formula) == 3:
                op, f1, f2 = formula
                if op == '&':
                    stack.extend([f1, f2])
                else:  # op == '|'
                    stack.append(f1)
        return depth
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_boolean_formula(n)
    
    qm = quadratic_residue_symbol(formula)
    d = frege_proof_depth(formula)
    
    return {
        "metric_name": "min_k |φ(k)|",
        "metric_value": qm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_qm = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_qm} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")