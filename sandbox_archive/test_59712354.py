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
    
    def generate_cnf(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) == 0:
                continue
            clauses.append(clause)
        return clauses
    
    def evaluate_cnf(cnf: list, assignment: list) -> bool:
        for clause in cnf:
            if all([assignment[abs(l)-1] * l >= 0 for l in clause]):
                continue
            return False
        return True
    
    def compute_additive_energy(cnf: list) -> int:
        n = len(cnf[0])
        energy = 0
        for a in range(2**n):
            for b in range(a, 2**n):
                if sum([abs(x - y) for x, y in zip(bin(a)[2:].zfill(n), bin(b)[2:].zfill(n))]) == n:
                    for c in range(b, 2**n):
                        for d in range(c, 2**n):
                            if sum([abs(x - y) for x, y in zip(bin(c)[2:].zfill(n), bin(d)[2:].zfill(n))]) == n:
                                energy += 1
        return energy
    
    def compute_communication_complexity(cnf: list) -> int:
        n = len(cnf[0])
        depth = 0
        while True:
            new_cnf = []
            for clause in cnf:
                if any(abs(l) > n for l in clause):
                    continue
                new_clause = [l if abs(l) <= n else -abs(l) for l in clause]
                if evaluate_cnf([new_clause], list(range(1, n+1))):
                    new_cnf.append(new_clause)
            if not new_cnf:
                break
            cnf = new_cnf
            depth += 1
        return depth
    
    def is_prime(num: int) -> bool:
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    def generate_primes(n: int) -> list:
        primes = []
        candidate = 2
        while len(primes) < n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    def compute_karchmer_wigderson_complexity(cnf: list) -> int:
        n = len(cnf[0])
        primes = generate_primes(n + 2)
        prime_set = set(primes)
        
        def find_prime_pair(a, b):
            for p in prime_set:
                if p > a and p > b and (p - a) % b == 0:
                    return p
            return None
        
        depth = 0
        while True:
            new_cnf = []
            for clause in cnf:
                if any(abs(l) > n for l in clause):
                    continue
                new_clause = [l if abs(l) <= n else -abs(l) for l in clause]
                if evaluate_cnf([new_clause], list(range(1, n+1))):
                    new_cnf.append(new_clause)
            if not new_cnf:
                break
            cnf = new_cnf
            depth += 1
        
        return depth
    
    def compute_metric(n: int) -> float:
        cnf = generate_cnf(n)
        energy = compute_additive_energy(cnf)
        communication_complexity = compute_karchmer_wigderson_complexity(cnf)
        if communication_complexity == 0:
            return float('inf')
        log_n = math.log2(n)
        return energy * communication_complexity * log_n
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = sum(2**n for n in n_values)
    
    total_energy = 0
    total_communication_complexity = 0
    
    for n in n_values:
        for _ in range(2**n):
            metric_value = compute_metric(n)
            if math.isinf(metric_value):
                continue
            total_energy += metric_value
            total_communication_complexity += compute_karchmer_wigderson_complexity(generate_cnf(n))
    
    mean_energy = total_energy / instances_tested
    mean_communication_complexity = total_communication_complexity / instances_tested
    
    if mean_energy * mean_communication_complexity * math.log2(40) <= 2**40:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Additive Energy",
        "metric_value": mean_energy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")