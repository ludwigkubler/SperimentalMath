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
    
    def generate_tseitin_formula(n, d):
        if n % d != 0:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * v for v in variables if v != i]
            clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        stack = list(clauses)
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    clause_i = set(abs(lit) for lit in stack[i])
                    clause_j = set(abs(lit) for lit in stack[j])
                    if len(clause_i & clause_j) == 1:
                        new_clause = [lit for lit in stack[i] if abs(lit) not in clause_j]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
    
    def minimal_order_of_modular_forms(clauses):
        # Placeholder implementation; actual computation depends on Hecke operators and lattices
        return len(clauses)
    
    n = random.randint(5, 30)
    d = random.randint(2, min(n - 1, 4))
    formula = generate_tseitin_formula(n, d)
    if formula is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    resolution_len = resolution_length(formula)
    modular_form_order = minimal_order_of_modular_forms(formula)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if "metric_value" in r) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")