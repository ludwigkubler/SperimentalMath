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
    
    def generate_tseitin(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f'-{variables[i-1]}', f'{variables[i-1]}'])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'-{variables[i-1]}', f'-{variables[j-1]}', f'{variables[i-1]}', f'{variables[j-1]}'])
        return variables, clauses
    
    def is_expander(G):
        n = len(G)
        degrees = [sum(1 for j in range(n) if G[i][j]) for i in range(n)]
        avg_degree = sum(degrees) / n
        return all(d >= 2 * avg_degree - 1 for d in degrees)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def resolution_length(G):
        n = len(G)
        clauses = [set(clause) for clause in G]
        unit_clauses = {c for c in clauses if len(c) == 1}
        while unit_clauses:
            new_unit_clauses = set()
            for u in unit_clauses:
                v = next(iter(u))
                for clause in clauses:
                    if v in clause:
                        clause.remove(v)
                        if len(clause) == 0:
                            return float('inf')
                        elif len(clause) == 1:
                            new_unit_clauses.add(clause)
            unit_clauses = new_unit_clauses
        return len([c for c in clauses if len(c) > 0])
    
    def symplectic_form_invariant(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = sum(1 for k in range(n) if G[i][k] and G[j][k])
                A[j][i] = A[i][j]
        U = gaussian_elimination(A)
        rank = sum(1 for row in U if any(row))
        return n - rank
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        candidate = 2
        while len(primes) < n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    def random_int(a, b):
        return a + random.randint(0, b - a)
    
    def random_bool():
        return bool(random.getrandbits(1))
    
    def random_matrix(n):
        A = [[random_bool() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = False
        return A
    
    def generate_random_tseitin_instance(n):
        variables, clauses = generate_tseitin(n)
        G = random_matrix(n)
        return G, variables, clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G, variables, clauses = generate_random_tseitin_instance(n)
        ν_G = symplectic_form_invariant(G)
        proof_length = resolution_length(G)
        results.append((ν_G, proof_length))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": float('nan'),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ν_Gs = [ν for ν, _ in results]
    proof_lengths = [L for _, L in results]
    
    mean_ν_G = sum(ν_Gs) / len(ν_Gs)
    std_ν_G = math.sqrt(sum((ν_G - mean_ν_G) ** 2 for ν_G in ν_Gs) / len(ν_Gs))
    correlation_coefficient = sum((ν_G - mean_ν_G) * (L - sum(proof_lengths) / len(proof_lengths)) for ν_G, L in results) / (len(results) * std_ν_G * math.sqrt(sum((L - sum(proof_lengths) / len(proof_lengths)) ** 2 for L in proof_lengths)))
    
    if correlation_coefficient < 0.8:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": mean_ν_G,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={correlation_coefficient}"
        }
    
    expander_results = [L for ν, L in results if is_expander(G)]
    non_expander_results = [L for ν, L in results if not is_expander(G)]
    
    mean_expander_L = sum(expander_results) / len(expander_results)
    std_expander_L = math.sqrt(sum((L - mean_expander_L) ** 2 for L in expander_results) / len(expander_results))
    mean_non_expander_L = sum(non_expander_results) / len(non_expander_results)
    std_non_expander_L = math.sqrt(sum((L - mean_non_expander_L) ** 2 for L in non_expander_results) / len(non_expander_results))
    
    if not (std_expander_L > 0 and std_non_expander_L == 0):
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": mean_ν_G,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"std_expander_L={std_expander_L}, std_non_expander_L={std_non_expander_L}"
        }
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_ν_G,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")