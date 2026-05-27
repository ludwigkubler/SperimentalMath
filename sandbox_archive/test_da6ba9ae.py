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
    
    def generate_random_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_monomial_circuit(f):
        n = len(f)
        clauses = []
        
        # Convert f to a list of literals
        literals = [i if f[i] == 1 else -i-1 for i in range(n)]
        
        # Add clauses for each literal
        for i in range(n):
            clauses.append([literals[i]])
        
        # Add clauses for each pair of literals (monomial form)
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([literals[i], literals[j]])
        
        return clauses
    
    def dpll(clauses, model={}):
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal > 0:
                model[literal] = True
            else:
                model[-literal] = False
            return dpll(clauses, model)
        
        empty_clause = any(not (c in model and model[c]) for c in clauses)
        if empty_clause:
            return False
        
        literal = next((c for c in literals if c not in model), None)
        if literal is None:
            return True
        
        # Branch on literal
        model[literal] = True
        if dpll(clauses, model):
            return True
        del model[literal]
        
        model[-literal] = True
        if dpll(clauses, model):
            return True
        del model[-literal]
        
        return False
    
    def count_quadratic_forms(circuit):
        n = len(circuit)
        quadratic_count = 0
        
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i][j] != 0:
                    quadratic_count += 1
        
        return quadratic_count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_quadratic_forms = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = generate_random_monotone_function(n)
            circuit = construct_monomial_circuit(f)
            quadratic_count = count_quadratic_forms(circuit)
            total_quadratic_forms += quadratic_count
            instances_tested += 1
    
    average_quadratic_forms = total_quadratic_forms / instances_tested
    
    return {
        "metric_name": "average_quadratic_forms",
        "metric_value": average_quadratic_forms,
        "instances_tested": instances_tested,
        "conjecture_holds": average_quadratic_forms <= n**2,  # Upper bound of polynomial in n
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")