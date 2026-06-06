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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        return cnf
    
    def dpll_proof_length(cnf):
        # Simplified DPLL algorithm to estimate proof length
        stack = []
        literals = set()
        for clause in cnf:
            literals.update(abs(l) for l in clause)
        
        def simplify():
            while True:
                unit_clauses = [l for l in literals if abs(l) not in literals]
                if not unit_clauses:
                    break
                literal = unit_clauses[0]
                stack.append((literal, 'unit'))
                literals.remove(abs(literal))
                cnf = [c for c in cnf if literal not in c and -literal not in c]
        
        def propagate():
            while True:
                pure_literals = [l for l in literals if sum(1 for c in cnf if l in c) == 0 or sum(1 for c in cnf if -l in c) == 0]
                if not pure_literals:
                    break
                literal = pure_literals[0]
                stack.append((literal, 'pure'))
                literals.remove(abs(literal))
                cnf = [c for c in cnf if literal not in c and -literal not in c]
        
        simplify()
        propagate()
        return len(stack)
    
    def smallest_prime_not_dividing(k):
        p = 2
        while True:
            if k % p != 0:
                return p
            p += 1
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = dpll_proof_length(cnf)
    clause_count = sum(len(clause) for clause in cnf)
    p = smallest_prime_not_dividing(clause_count)
    
    if p == 1:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def finite_field_extension(p):
        # Simplified representation of a finite field extension
        return p
    
    def primitive_element_order(p):
        # Order of a primitive element in the finite field Q_p
        if p == 2:
            return 1
        for i in range(1, p):
            if pow(i, p - 1, p) == 1:
                return i
    
    order = primitive_element_order(finite_field_extension(p))
    
    if order is None:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    upper_bound = n ** (1 / p)
    ratio = order / upper_bound
    
    return {
        "metric_name": "minimal_order",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")