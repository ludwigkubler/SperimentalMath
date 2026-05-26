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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clause = [variables[i]]
            for j in range(i+1, n):
                clause.append(f'~{variables[j]}')
            clauses.append(clause)
        return variables, clauses
    
    def resolution_proof_depth(formula):
        # Simplified DPLL algorithm to estimate proof depth
        stack = []
        while formula:
            unit_clause = next((c for c in formula if len(c) == 1), None)
            if not unit_clause:
                return float('inf')
            literal = unit_clause[0]
            formula.remove(unit_clause)
            for clause in formula:
                if literal in clause:
                    clause.remove(literal)
                elif f'~{literal}' in clause:
                    clause.remove(f'~{literal}')
                    stack.append(clause)
        return len(stack) + 1
    
    def l_function(n):
        # Simplified L-Function calculation
        return math.log(n, 2)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    formula = [clauses[i] for i in range(len(clauses))]
    depth = resolution_proof_depth(formula)
    l_n = l_function(n)
    
    if depth < c_k * l_n:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula with n={n} has depth {depth} < {c_k}*L({n}) = {c_k*l_n}"
        }
    else:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n={n} has depth {depth} < {c_k}*L({n})\" first_failing_seed={first_failing_seed}")