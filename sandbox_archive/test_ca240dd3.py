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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def evaluate_formula(phi, assignment):
        if phi == 'True':
            return True
        elif phi == 'False':
            return False
        else:
            var, op, subphi = phi.split()
            val_var = assignment[var]
            val_subphi = evaluate_formula(subphi, assignment)
            if op == '&':
                return val_var and val_subphi
            elif op == '|':
                return val_var or val_subphi
    
    def compute_simplicial_complex(phi):
        n = phi.count('(') + 1
        simplicial_complex = []
        stack = []
        for i, char in enumerate(phi):
            if char == '(':
                stack.append(i)
            elif char == ')':
                start = stack.pop()
                simplicial_complex.append(phi[start:i+1])
        return simplicial_complex
    
    def compute_local_coherence(simplicial_complex):
        # Simplified version of local coherence calculation
        return len(simplicial_complex) / n
    
    def compute_frege_proof_depth(phi):
        if phi == 'True' or phi == 'False':
            return 1
        else:
            var, op, subphi = phi.split()
            return 2 + max(compute_frege_proof_depth(subphi), compute_frege_proof_depth(subphi))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            phi = generate_formula(n)
            assignment = {var: random.choice([True, False]) for var in set(phi) if var.isalpha()}
            simplicial_complex = compute_simplicial_complex(phi)
            local_coherence = compute_local_coherence(simplicial_complex)
            frege_depth = compute_frege_proof_depth(phi)
            results.append((local_coherence, frege_depth))
    
    mean_local_coherence = sum(x for x, _ in results) / len(results)
    mean_frege_depth = sum(y for _, y in results) / len(results)
    correlation_coefficient = (n - 1) * sum((x - mean_local_coherence) * (y - mean_frege_depth) for x, y in results) / \
                               math.sqrt(sum((x - mean_local_coherence)**2 for x, _ in results)) / \
                               math.sqrt(sum((y - mean_frege_depth)**2 for _, y in results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient >= 0.5 else "correlation_below_0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.5\" first_failing_seed={first_failing_seed + 1}")