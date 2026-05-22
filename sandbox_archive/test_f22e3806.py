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

def is_quadratic_residue(a, p):
    return pow(a, (p - 1) // 2, p) == 1

def count_quadratic_residues(n):
    return sum(is_quadratic_residue(i, n) for i in range(1, n))

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([variables[i]])
        for j in range(i + 1, n):
            clauses.append([-variables[i], -variables[j]])
            clauses.append([variables[i], variables[j]])
    return clauses

def resolution_length(clauses):
    stack = [clauses]
    while stack:
        clause = stack.pop()
        if not clause:
            return len(stack)
        literal = next(l for l in clause if l > 0)
        new_clauses = []
        for c in stack:
            if -literal in c:
                continue
            new_c = [l for l in c if l != literal]
            if not new_c:
                return len(stack)
            new_clauses.append(new_c)
        stack.extend(new_clauses)
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        quadratic_residues_count = count_quadratic_residues(n)
        expected_length = Fraction(n**2 * math.log(n, quadratic_residues_count), math.log(math.log(n, quadratic_residues_count)))
        
        if quadratic_residues_count == 0:
            return {
                "metric_name": "Resolution Proof Length",
                "metric_value": float('inf'),
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "quadratic_residues_count_undefined"
            }
        
        for _ in range(5):
            formula = generate_tseitin_formula(n)
            length = resolution_length(formula)
            results.append(length)
    
    mean_length = sum(results) / len(results)
    support_fraction = sum(1 for length in results if expected_length * 0.9 <= length <= expected_length * 1.1) / len(results)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_length={mean_length}, expected_length={expected_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")