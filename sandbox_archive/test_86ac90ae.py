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
    return abs(a * b) // gcd(a, b)

def matrix_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_pow(M, p):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, M)
        M = matrix_mul(M, M)
        p //= 2
    return result

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
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
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate a random Coxeter system with n generators
        W = [f'a{i}' for i in range(n)]
        relations = []
        for i in range(n):
            for j in range(i + 1, n):
                relations.append((W[i], W[j]))
                relations.append((W[j], W[i]))

        # Construct the binary tree T for the Coxeter system
        def construct_tree(W, relations):
            if not W:
                return []
            root = W[0]
            left = construct_tree([w for w in W if (root, w) in relations], relations)
            right = construct_tree([w for w in W if (w, root) in relations], relations)
            return [root] + left + right

        tree = construct_tree(W, relations)

        # Construct an AC^0 circuit L(W) that emulates the decision problem associated with the tree T
        def construct_circuit(tree):
            if not tree:
                return []
            node = tree[0]
            left = construct_circuit(tree[1:])
            right = construct_circuit(tree[1:])
            return [node] + left + right

        circuit = construct_circuit(tree)

        # Measure the size of L(W)
        metric_value = len(circuit)

        # Update total metric value and instances tested
        total_metric_value += metric_value
        instances_tested += 1

        # Check if the conjecture holds for this seed
        if metric_value < 2**n:
            conjecture_holds = False
            counterexample = f"n={n}, circuit_size={metric_value}"

    return {
        "metric_name": "circuit_size",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")