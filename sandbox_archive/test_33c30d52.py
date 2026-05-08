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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_3cnf(n, m, alpha):
    clauses = set()
    while len(clauses) < m:
        clause = [random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)]
        if all(abs(c) != abs(d) for c in clause for d in clause[1:]) and all(abs(c) <= n for c in clause):
            clauses.add(tuple(sorted(clause)))
    return clauses

def is_unsatisfiable(phi):
    n = max(abs(x) for x, y, z in phi)
    cube = [(i, j, k) for i in range(2) for j in range(2) for k in range(2)]
    for assignment in cube:
        if all((x + 1 if a else -a) not in clause for a, x, y, z in phi):
            return False
    return True

def f_phi(phi, n):
    m = len(phi)
    count = sum(1 for x in range(2**n) if any(all((x >> i & 1) + 1 if a else -(a + 1) not in clause for a, *clause in phi) for i in range(n)))
    return count / m

def g_phi(phi, n):
    f_n = f_phi(phi, n)
    return [f_phi(phi, n) - f_n for _ in range(2**n)]

def norm_4(g):
    return sum(x**4 for x in g)**0.25

def norm_2(g):
    return sum(x**2 for x in g)**0.5

def dpll_up(phi, assignment=[]):
    if len(assignment) == n:
        return 1
    var = next((i for i in range(n) if all(abs(a) != abs(i+1) for a, *clause in phi)), None)
    if var is None:
        return 0
    count = 0
    for val in [0, 1]:
        new_assignment = assignment + [(var + 1) if val else -(var + 1)]
        count += dpll_up(phi, new_assignment)
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    m = int(4.5 * n)
    alpha = 4.5
    instances_tested = 0
    total_t_dpll = 0
    per_instance_bounds = []
    
    for n in n_values:
        phi = random_3cnf(n, m, alpha)
        if not is_unsatisfiable(phi):
            continue
        
        f_n = f_phi(phi, n)
        g_n = g_phi(phi, n)
        norm_g4 = norm_4(g_n)
        norm_g2 = norm_2(g_n)
        E = norm_g4 / norm_g2 if norm_g2 != 0 else 1
        T_dpll = dpll_up(phi)
        
        instances_tested += 1
        total_t_dpll += T_dpll
        per_instance_bounds.append((T_dpll, (n - math.log2(m)) / E - 5))
    
    if instances_tested == 0:
        return {
            "metric_name": "log2_T",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances found"
        }
    
    log2_T_mean = math.log2(total_t_dpll / instances_tested)
    log2_T_values = [math.log2(T) for T, _ in per_instance_bounds]
    E_values = [(n - math.log2(m)) / (norm_4(g_phi(random_3cnf(n, m, alpha), n)) / norm_2(g_phi(random_3cnf(n, m, alpha), n))) if norm_2(g_phi(random_3cnf(n, m, alpha), n)) != 0 else 1 for _ in range(instances_tested)]
    
    rho = sum((log2_T_values[i] - sum(log2_T_values) / instances_tested) * (E_values[i] - sum(E_values) / instances_tested) for i in range(instances_tested)) / ((sum((log2_T_values[i] - sum(log2_T_values) / instances_tested)**2 for i in range(instances_tested)) * sum((E_values[i] - sum(E_values) / instances_tested)**2 for i in range(instances_tested)))**0.5)
    
    conjecture_holds = all(T >= E - 5 for T, E in per_instance_bounds) and rho >= 0.5
    counterexample = "" if conjecture_holds else "rho < 0.5 or some instance violates the bound"
    
    return {
        "metric_name": "log2_T",
        "metric_value": log2_T_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    mean_log2_T = sum(r["metric_value"] for r in results) / len(results)
    std_log2_T = (sum((r["metric_value"] - mean_log2_T)**2 for r in results) / len(results))**0.5
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log2_T} std={std_log2_T} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")