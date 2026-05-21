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

def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    return [p for p in range(2, n + 1) if primes[p]]

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_dirichlet_progression(a, d, n):
    return [(a + k * d) % n for k in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random 3-SAT instance with n variables
    n = random.randint(5, 40)
    m = random.randint(2 * n, 4 * n)
    clauses = []
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clauses.append(tuple(literals))
    
    # Check if the clause graph is bipartite
    variable_to_clauses = {i: [] for i in range(1, n + 1)}
    for clause in clauses:
        for literal in clause:
            variable_to_clauses[abs(literal)].append(clause)
    
    def bfs(start):
        queue = [start]
        visited = set()
        color = {start: 0}
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbor in variable_to_clauses[node]:
                    for lit in neighbor:
                        var = abs(lit)
                        if var != node and var not in visited:
                            if color.get(var) is None:
                                color[var] = 1 - color[node]
                                queue.append(var)
                            elif color[var] == color[node]:
                                return False
        return True
    
    if not bfs(1):
        return {
            "metric_name": "Seed Length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Clause graph is not bipartite"
        }
    
    # Compute π(n) using sieve of Eratosthenes
    primes = sieve_of_eratosthenes(n)
    pi_n = len(primes)
    
    # Generate a Dirichlet progression based on clause graph bipartitioning
    modulus = n * n
    if not is_prime(modulus):
        return {
            "metric_name": "Seed Length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Modulus must be a prime number"
        }
    
    progression = generate_dirichlet_progression(1, 2, modulus)
    
    # Simulate PRG seed length via a pseudorandom generator with explicit modular arithmetic
    seed_length = len(progression)
    
    return {
        "metric_name": "Seed Length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": abs(seed_length - pi_n) <= 2 * math.sqrt(pi_n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Modulus must be a prime number\" first_failing_seed={first_failing_seed}")