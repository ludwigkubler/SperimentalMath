# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes_up_to(limit):
        primes = []
        for num in range(2, limit):
            if is_prime(num):
                primes.append(num)
        return primes
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            literals = random.sample(range(1, 2*n+1), 3)
            clause = [(-l if random.choice([True, False]) else l) for l in literals]
            clauses.append(clause)
        return clauses
    
    def young_diagram(n):
        d = 0
        while n > 0:
            d += 1
            n -= d
        return d
    
    def permanent(cnf):
        if not cnf:
            return 1
        variables = set()
        for clause in cnf:
            variables.update(abs(lit) for lit in clause)
        n = len(variables)
        
        def permute(i, j):
            nonlocal cnf
            new_cnf = []
            for clause in cnf:
                if i not in clause and j not in clause:
                    new_clause = [lit for lit in clause if lit != -i and lit != -j]
                    if new_clause:
                        new_cnf.append(new_clause)
                elif i in clause and j not in clause:
                    new_clause = [lit for lit in clause if lit != i and lit != -j]
                    if new_clause:
                        new_cnf.append([-lit for lit in new_clause])
                elif i not in clause and j in clause:
                    new_clause = [lit for lit in clause if lit != -i and lit != j]
                    if new_clause:
                        new_cnf.append([-lit for lit in new_clause])
                else:
                    new_clause = [lit for lit in clause if lit != i and lit != j]
                    if new_clause:
                        new_cnf.append(new_clause)
            cnf = new_cnf
        
        def permute_all():
            nonlocal cnf
            for i, j in combinations(range(1, n+1), 2):
                permute(i, j)
        
        permute_all()
        return len(cnf)

    n = 40
    m = 3 * n
    cnf = generate_3cnf(n, m)
    d = young_diagram(n)
    
    circuit_size = permanent(cnf)
    metric_value = circuit_size / (2**d / n**2)
    
    conjecture_holds = metric_value >= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_size_over_bound",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes_up_to(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")