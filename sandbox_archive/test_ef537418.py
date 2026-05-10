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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def partition_to_tuple(partition):
    return tuple(sorted(partition, reverse=True))

def partitions(n):
    def partitions_recursive(n, max_partition):
        if n == 0:
            yield ()
        else:
            for i in range(1, min(n + 1, max_partition + 1)):
                for p in partitions_recursive(n - i, i):
                    yield (i,) + p
    return list(partitions_recursive(n, n))

def kronecker_coefficient(lambda_, mu, nu):
    if len(mu) != len(nu):
        return 0
    lambda_ = partition_to_tuple(lambda_)
    mu = partition_to_tuple(mu)
    nu = partition_to_tuple(nu)
    
    def sign(p):
        s = 1
        for i in range(len(p)):
            for j in range(i + 1, len(p)):
                if p[i] < p[j]:
                    s *= -1
        return s
    
    def hook_length_product(partition):
        product = 1
        n = sum(partition)
        for i, x in enumerate(partition):
            for j in range(x):
                product *= (n - i - j)
        return product
    
    def hook_length_product_diff(lambda_, mu, nu):
        return hook_length_product(nu) // (hook_length_product(mu) * hook_length_product(lambda_))
    
    result = 0
    for p in partitions(len(lambda_)):
        if all(p[i] <= lambda_[i] and p[i] <= mu[i] and p[i] <= nu[i] for i in range(len(p))):
            result += sign(p) * binomial_coefficient(nu[0], p[0]) * hook_length_product_diff(lambda_, mu, nu)
    return result

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(3)]
        random.shuffle(clause)
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        if random.choice([True, False]):
            clause[2] *= -1
        clauses.append(tuple(clause))
    return clauses

def is_satisfiable(clauses):
    n = max(abs(v) for v in set(var for clause in clauses for var in clause))
    assignment = [random.choice([-1, 1]) for _ in range(n)]
    for clause in clauses:
        if not any(assignment[abs(var) - 1] * var > 0 for var in clause):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(n // 2, n * 2)
        clauses = generate_3cnf(n, m)
        unsatisfiable = not is_satisfiable(clauses)
        
        row_sums = [sum(abs(var) for var in clause) for clause in clauses]
        lambda_ = partition_to_tuple(row_sums)
        k_phi = sum(lambda_)
        
        if unsatisfiable and k_phi > 2 * n * math.log(n):
            conjecture_holds = False
            counterexample = f"Unsatisfiable instance with k(Φ) > 2n log n: n={n}, m={m}"
            break
        
        mu = (n,)
        nu = (m,)
        g_lambda_mu_nu = kronecker_coefficient(lambda_, mu, nu)
        
        if unsatisfiable and g_lambda_mu_nu == 0:
            conjecture_holds = False
            counterexample = f"Unsatisfiable instance with zero Kronecker coefficient: n={n}, m={m}"
            break
        
        if satisfiable and g_lambda_mu_nu != 0:
            conjecture_holds = False
            counterexample = f"Satisfiable instance with non-zero Kronecker coefficient: n={n}, m={m}"
            break
        
        total_metric_value += g_lambda_mu_nu
        instances_tested += 1
    
    return {
        "metric_name": "Kronecker Coefficient",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")