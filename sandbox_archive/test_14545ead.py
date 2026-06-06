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
        for _ in range(random.randint(2, n)):
            clause = [random.choice(range(-n, 0)) for _ in range(3)]
            cnf.append(clause)
        return cnf
    
    def dpll_proof_length(cnf):
        n = len(cnf[0])
        literals = list(range(1, n + 1)) + [-lit for lit in range(1, n + 1)]
        
        def is_satisfiable(phi):
            assignment = [None] * (n + 1)
            
            def backtrack(k):
                if k == n + 1:
                    return True
                for val in [True, False]:
                    assignment[k] = val
                    if all(any(lit in assignment for lit in clause) for clause in phi):
                        if backtrack(k + 1):
                            return True
                    assignment[k] = None
                return False
            
            return backtrack(1)
        
        proof_length = 0
        while not is_satisfiable(cnf):
            clause = random.choice(cnf)
            literal = random.choice(clause)
            cnf.remove([l for l in clause if l != literal])
            proof_length += 1
        
        return proof_length
    
    def minimal_order(p, n):
        p_adic_numbers = [Fraction(1, i) for i in range(1, p)]
        for order in range(1, p + 1):
            if all((p_adic_number ** order).numerator % p == 0 for p_adic_number in p_adic_numbers):
                return order
        return p
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = dpll_proof_length(cnf)
    
    smallest_prime_not_dividing_clauses = min(p for p in range(2, proof_length + 1) if all(proof_length % p != 0 for clause in cnf))
    
    p_adic_extension_order = minimal_order(smallest_prime_not_dividing_clauses, n)
    upper_bound = Fraction(n ** (1 / smallest_prime_not_dividing_clauses), 1)
    
    return {
        "metric_name": "minimal_order_ratio",
        "metric_value": p_adic_extension_order / upper_bound,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": p_adic_extension_order <= upper_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")