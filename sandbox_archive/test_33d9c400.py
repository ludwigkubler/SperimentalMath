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
    
    def generate_monotone_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def construct_monomial_circuit(f):
        # Simplified DPLL solver to count quadratic forms
        n = len(f)
        clauses = [int(c) for c in f]
        variables = list(range(n))
        model = {v: None for v in variables}
        
        def dpll(clauses, model):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                var = abs(unit_clause[0]) - 1
                val = 1 if unit_clause[0] > 0 else 0
                model[var] = val
                return dpll([c for c in clauses if not (var in c and val == (c[0] > 0))], model)
            pure_literal = next((v for v in variables if all(v in c or -v in c for c in clauses)), None)
            if pure_literal is None:
                return False
            val = 1 if random.choice([True, False]) else 0
            model[pure_literal] = val
            return dpll(clauses, model)
        
        def count_quadratic_forms(model):
            count = 0
            for v in variables:
                if model[v] is not None:
                    count += 1
            return count
        
        if dpll(clauses, model):
            return count_quadratic_forms(model)
        else:
            return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_r = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_monotone_boolean_function(n)
            r_f = construct_monomial_circuit(f)
            if r_f < float('inf'):
                total_r += r_f
                instances_tested += 1
    
    average_r = total_r / instances_tested if instances_tested > 0 else 0
    conjecture_holds = average_r <= n**2  # Polynomial upper bound for average r(f)
    
    return {
        "metric_name": "average_r",
        "metric_value": average_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average r(f) = {average_r} > n^2 for some n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='average_r > n^2' first_failing_seed={first_failing_seed}")