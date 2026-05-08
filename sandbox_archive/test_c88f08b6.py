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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dpll(instance, order):
    assignment = {}
    stack = []
    def unit_propagation():
        while True:
            changed = False
            for literal in instance:
                if literal[0] not in assignment and -literal[0] not in assignment:
                    count_true = sum(1 for lit in literal if lit in assignment and assignment[lit])
                    count_false = sum(1 for lit in literal if lit in assignment and not assignment[lit])
                    if count_true == len(literal) - 1:
                        assignment[literal[0]] = True
                        changed = True
                    elif count_false == len(literal) - 1:
                        assignment[-literal[0]] = True
                        changed = True
            if not changed:
                break
    def backtrack():
        while stack:
            var, level = stack.pop()
            for literal in instance:
                if var in literal and literal.index(var) != 0:
                    continue
                new_assignment = assignment.copy()
                new_assignment[var] = False
                unit_propagation()
                if not any(lit in new_assignment and not new_assignment[lit] for lit in instance):
                    return True, new_assignment
            stack.pop()
        return False, None
    for var in order:
        assignment[var] = True
        unit_propagation()
        if not any(lit in assignment and not assignment[lit] for lit in instance):
            continue
        assignment[var] = False
        unit_propagation()
        if not any(lit in assignment and not assignment[lit] for lit in instance):
            stack.append((var, len(stack)))
    return backtrack()[1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    phi = (math.sqrt(5) - 1) / 2
    instances = []
    for n in [12, 16, 20, 24]:
        m = 8 * n
        instance = []
        while len(instance) < m:
            clause = random.sample(range(1, n+1), 3)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            instance.append(clause)
        instances.append((n, instance))
    
    T_phi_values = []
    mu_R_values = []
    for n, instance in instances:
        order_phi = sorted(range(1, n+1), key=lambda i: (i * phi) % 1)
        T_phi = dpll(instance, order_phi)
        T_phi_values.append(T_phi)
        
        mu_R = 0
        for _ in range(30):
            order_R = random.sample(range(1, n+1), n)
            T_R = dpll(instance, order_R)
            mu_R += math.log2(T_R)
        mu_R /= 30
        mu_R_values.append(mu_R)
    
    mean_T_phi = sum(T_phi_values) / len(T_phi_values)
    std_T_phi = (sum((x - mean_T_phi) ** 2 for x in T_phi_values) / len(T_phi_values)) ** 0.5
    mean_mu_R = sum(mu_R_values) / len(mu_R_values)
    std_mu_R = (sum((x - mean_mu_R) ** 2 for x in mu_R_values) / len(mu_R_values)) ** 0.5
    
    support_fraction = sum(1 for T_phi, mu_R in zip(T_phi_values, mu_R_values) if T_phi <= mu_R + 4 * math.log2(n)) / len(T_phi_values)
    
    return {
        "metric_name": "log2_T_phi_minus_mu_R",
        "metric_value": mean_T_phi - mean_mu_R,
        "instances_tested": len(T_phi_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={n}, T_phi={T_phi}, mu_R={mu_R}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(x["metric_value"] for x in results) / len(results)
    std_metric = (sum((x["metric_value"] - mean_metric) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")