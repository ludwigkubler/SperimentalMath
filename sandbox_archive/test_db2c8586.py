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

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def generate_projective_plane(q):
    if q < 2 or not is_prime(q):
        raise ValueError("q must be a prime number greater than 1")
    points = [(x, y) for x in range(q) for y in range(q)]
    lines = []
    for i in range(q):
        line = [(i + x, (i * x) % q) for x in range(q)]
        lines.append(line)
    for a in range(1, q):
        for b in range(q):
            if math.gcd(a, q - 1) == 1:
                line = [(a * x + b, (a * x + b) % q) for x in range(q)]
                lines.append(line)
    return points, lines

def simulate_communication_complexity(n, q):
    points, lines = generate_projective_plane(q)
    num_lines = len(lines)
    communication_cost = 0
    for _ in range(n):
        subset1 = random.sample(range(num_lines), random.randint(1, num_lines))
        subset2 = random.sample(range(num_lines), random.randint(1, num_lines))
        intersection = set(subset1).intersection(set(subset2))
        if len(intersection) > 0:
            communication_cost += math.log(q, 2)
    return communication_cost / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2, 3, 4]
    results = []
    for q in q_values:
        communication_cost = simulate_communication_complexity(30, q)
        expected_cost = q**2 * math.log(q, 2)
        if abs(communication_cost - expected_cost) / expected_cost > 0.1:
            return {
                "metric_name": "Communication Cost",
                "metric_value": communication_cost,
                "instances_tested": 30,
                "conjecture_holds": False,
                "counterexample": f"q={q}, observed={communication_cost}, expected={expected_cost}"
            }
        results.append(communication_cost)
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    return {
        "metric_name": "Communication Cost",
        "metric_value": mean,
        "instances_tested": 30 * len(q_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0.9 * mean and r < 1.1 * mean) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (result > 0.9 * mean and result < 1.1 * mean))
        print(f"RESULT: FALSIFIED counterexample=\"communication_cost_outside_bounds\" first_failing_seed={first_failing_seed}")