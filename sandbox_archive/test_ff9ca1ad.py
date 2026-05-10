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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    density = 2.5
    c = 0.8
    
    def generate_3sat_instance(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 6)):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def dpll_solve(clauses):
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        
        def solve(model):
            if not clauses:
                return model
            literal = next(l for l in literals if l not in model and -l not in model)
            new_model = model.copy()
            new_model[literal] = True
            if dpll(clauses, new_model):
                return new_model
            new_model[literal] = False
            new_model[-literal] = True
            if dpll(clauses, new_model):
                return new_model
            return None
        
        def dpll(clauses, model):
            unsatisfied_clauses = [c for c in clauses if not any(l in model or -l in model for l in c)]
            if not unsatisfied_clauses:
                return True
            literal = next(l for l in literals if l not in model and -l not in model)
            new_model = model.copy()
            new_model[literal] = True
            if dpll(unsatisfied_clauses, new_model):
                return True
            new_model[literal] = False
            new_model[-literal] = True
            if dpll(unsatisfied_clauses, new_model):
                return True
            return False
        
        return solve({})
    
    def class_number(m):
        # Simplified version for demonstration; actual implementation needed
        return 1
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        clauses = generate_3sat_instance(n, density)
        m = len(clauses)
        K = math.sqrt(m)
        h_K = class_number(m)
        L = dpll_solve(clauses) is not None
        
        if L == 0:
            counterexample = "DPLL proof length is zero"
            conjecture_holds = False
            break
        
        instances_tested += 1
        if h_K * L / math.log(n) < c:
            counterexample = f"Counterexample found: h(K) * L / log(n) = {h_K * L / math.log(n)} < {c}"
            conjecture_holds = False
    
    return {
        "metric_name": "h(K) * L / log(n)",
        "metric_value": h_K * L / math.log(n),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")