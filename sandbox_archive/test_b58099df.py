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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[pivot_row][i]):
                pivot_row = j
        M[i], M[pivot_row] = M[pivot_row], M[i]
        for j in range(n):
            if j != i:
                factor = M[j][i] / M[i][i]
                for k in range(n+1):
                    M[j][k] -= factor * M[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j]*x[j] for j in range(i+1, n))) / M[i][i]
    return x

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

def generate_primes(min_val, max_val):
    primes = []
    for num in range(min_val, max_val + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_dfa(n):
    states = list(range(n))
    alphabet = [0, 1]
    transitions = {i: {a: random.choice(states) for a in alphabet} for i in states}
    initial_state = random.choice(states)
    accepting_states = set(random.sample(states, random.randint(1, n)))
    return (states, alphabet, transitions, initial_state, accepting_states)

def syntactic_monoid(dfa):
    states, _, transitions, initial_state, _ = dfa
    n = len(states)
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    for _ in range(2*n):
        M = matrix_mult(M, transitions)
    return sum(sum(row) for row in M)

def resolution_steps(dfa):
    states, _, transitions, initial_state, accepting_states = dfa
    n = len(states)
    clauses = []
    for i in range(n):
        if i not in accepting_states:
            clauses.append([i])
    for a in [0, 1]:
        for i in range(n):
            for j in range(n):
                if transitions[i][a] != j and (j not in accepting_states or i in accepting_states):
                    clauses.append([-i, -j])
    while True:
        new_clauses = []
        for clause1 in clauses:
            for clause2 in clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = list(set(clause1 + clause2) - {list(set(clause1) & set(clause2))[0]})
                    if new_clause not in new_clauses and new_clause not in clauses:
                        new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.extend(new_clauses)
    return len(clauses)

def resolution_depth(dfa):
    states, _, transitions, initial_state, accepting_states = dfa
    n = len(states)
    depth = [0]*n
    for i in range(n):
        if i not in accepting_states:
            depth[i] = 1
        else:
            for a in [0, 1]:
                for j in range(n):
                    if transitions[i][a] != j and (j not in accepting_states or i in accepting_states):
                        depth[j] = max(depth[j], depth[i] + 1)
    return max(depth)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_steps = 0
    total_depth = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            dfa = generate_dfa(n)
            rank = syntactic_monoid(dfa)
            steps = resolution_steps(dfa)
            depth = resolution_depth(dfa)
            if rank <= n:
                total_steps += steps
                total_depth += depth
                instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "Ratio of Resolution Steps to Depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }

    ratio = Fraction(total_steps, total_depth)
    return {
        "metric_name": "Ratio of Resolution Steps to Depth",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} > 1"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(2, 30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    print(f"RESULT: {'SUPPORTED' if support_fraction == 1.0 else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")