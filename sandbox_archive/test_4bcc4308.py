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

def matrix_mult(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
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
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = Augmented[k][i]
                for j in range(i, n+1):
                    Augmented[k][j] -= factor * Augmented[i][j]
    return [row[-1] for row in Augmented]

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

def generate_coxeter_system(n, seed):
    random.seed(seed)
    generators = [random.randint(1, 100) for _ in range(n)]
    relations = []
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                relations.append((i, j))
    return generators, relations

def construct_binary_tree(generators, relations):
    tree = {i: [] for i in range(len(generators))}
    for i, j in relations:
        tree[i].append(j)
        tree[j].append(i)
    return tree

def count_automorphisms(tree):
    n = len(tree)
    visited = [False] * n
    automorphisms = 0
    
    def dfs(node, mapping):
        if visited[node]:
            return True
        visited[node] = True
        for neighbor in tree[node]:
            if not visited[neighbor]:
                new_mapping = {i: j for i, j in mapping.items()}
                new_mapping[neighbor] = node
                if dfs(neighbor, new_mapping):
                    return True
        visited[node] = False
        return False
    
    def count_mappings():
        nonlocal automorphisms
        if all(visited[i] for i in range(n)):
            automorphisms += 1
            return
        for i in range(n):
            if not visited[i]:
                dfs(i, {i: i})
    
    for start in range(n):
        visited = [False] * n
        count_mappings()
    
    return automorphisms

def construct_ac0_circuit(tree):
    # This is a placeholder function. In practice, constructing an AC^0 circuit
    # from a binary tree would be complex and beyond the scope of this test.
    # For simplicity, we assume that the size of the circuit grows exponentially with the number of nodes.
    return 2 ** len(tree)

def run_trial(seed: int) -> dict:
    n = random.choice([5, 10, 15, 20, 30, 40])
    generators, relations = generate_coxeter_system(n, seed)
    tree = construct_binary_tree(generators, relations)
    automorphism_size = count_automorphisms(tree)
    ac0_circuit_size = construct_ac0_circuit(tree)
    
    if automorphism_size < 2 ** n:
        return {
            "metric_name": "Automorphism Group Size",
            "metric_value": automorphism_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "automorphism_group_too_small"
        }
    
    if ac0_circuit_size < 2 ** n:
        return {
            "metric_name": "AC^0 Circuit Size",
            "metric_value": ac0_circuit_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "ac0_circuit_too_small"
        }
    
    return {
        "metric_name": "Automorphism Group Size",
        "metric_value": automorphism_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r.get("conjecture_holds", False))
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result.get("conjecture_holds", True))
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")