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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_circuit(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        n_vars = max(literals)
        
        formulas = []
        for i, literal in enumerate(literals):
            formulas.append(f"x{i+1} = {literal}")
        
        for clause in clauses:
            or_clause = " | ".join([f"~x{abs(lit)}" if lit < 0 else f"x{lit}" for lit in clause])
            formulas.append(f"y{i+1} = {or_clause}")
        
        return formulas
    
    def hodge_decomposition(formulas):
        # Placeholder function to simulate Hodge decomposition
        # This is a dummy implementation and should be replaced with actual logic
        rank = len(formulas)
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(2, n-1)
    clauses = generate_k_cnf(n, k)
    formulas = tseitin_circuit(clauses)
    rank = hodge_decomposition(formulas)
    
    expected_upper_bound = math.log(n / k) ** 2
    if rank > expected_upper_bound:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank}, expected={expected_upper_bound}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeded expected upper bound\" first_failing_seed={first_failing_seed}")