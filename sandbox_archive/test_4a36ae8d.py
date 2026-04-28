# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d:
            d += 1
        else:
            n //= d
            factors.append(d)
    if n > 1:
        factors.append(n)
    return factors

def phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def generate_random_truth_table(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def evaluate_circuit(circuit, truth_table):
    stack = []
    for gate in circuit:
        if gate == 'AND':
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        elif gate == 'NOT':
            a = stack.pop()
            stack.append(not a)
        else:
            stack.append(truth_table[gate])
    return stack[0]

def generate_sym_and_circuit(s, n):
    circuit = []
    for _ in range(s):
        if random.choice([True, False]):
            circuit.append('NOT')
        else:
            circuit.append(random.randint(0, 2**n - 1))
    circuit.append('AND')
    return circuit

def generate_majority_circuit(n):
    circuit = ['NOT'] * n + [random.randint(0, 2**n - 1)] * (n // 2) + ['OR'] * (n // 2)
    random.shuffle(circuit)
    return circuit

def generate_random_sym_and_circuits(s, n):
    circuits = []
    for _ in range(s):
        if random.choice([True, False]):
            circuit = generate_majority_circuit(n)
        else:
            circuit = generate_sym_and_circuit(s, n)
        circuits.append(circuit)
    return circuits

def compute_alpha_f(truth_table, m):
    n = int(math.log2(len(truth_table)))
    zeta_m = [complex(math.cos(2 * math.pi * k / m), math.sin(2 * math.pi * k / m)) for k in range(m)]
    alpha_f = 0
    for x in truth_table:
        k = sum(x[i] * (1 << i) for i in range(n))
        alpha_f += x * zeta_m[k % m]
    return alpha_f / (2 ** n)

def compute_cyclotomic_norm(alpha_f):
    m = len(zeta_m)
    regular_rep_matrix = [[alpha_f**(i * j) for j in range(m)] for i in range(m)]
    det = 1
    for i in range(m):
        det *= regular_rep_matrix[i][i]
        for j in range(i + 1, m):
            factor = regular_rep_matrix[j][i] / regular_rep_matrix[i][i]
            for k in range(m):
                regular_rep_matrix[j][k] -= factor * regular_rep_matrix[i][k]
    return abs(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [6, 10, 15]
    n_values = [8, 10, 12, 14]
    s_values = [4, 8, 16, 32, 64]
    results = []

    for m in m_values:
        if len(prime_factors(m)) < 2:
            continue
        for n in n_values:
            for s in s_values:
                for _ in range(400):
                    if random.choice([True, False]):
                        circuit = generate_random_sym_and_circuits(s, n)
                        truth_table = generate_truth_table(n)
                    else:
                        circuit = generate_majority_circuit(n)
                        truth_table = [random.randint(0, 1) for _ in range(2**n)]
                    alpha_f = compute_alpha_f(truth_table, m)
                    norm = compute_cyclotomic_norm(alpha_f)
                    results.append((m, n, s, -math.log2(norm), len(circuit)))

    slope_sum = 0
    residual_sum = 0
    count = 0

    for m in m_values:
        if len(prime_factors(m)) < 2:
            continue
        for n in n_values:
            data = [(s, y) for _, _, s, y, _ in results if m == m and n == n]
            if len(data) >= 400:
                x_vals = [math.log2(s) for s, _ in data]
                y_vals = [y for _, y in data]
                mean_x = sum(x_vals) / len(x_vals)
                mean_y = sum(y_vals) / len(y_vals)
                slope = (sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals)) /
                         sum((x - mean_x)**2 for x in x_vals))
                residuals = [y - (slope * (x - mean_x) + mean_y) for x, y in zip(x_vals, y_vals)]
                residual_sum += sorted(residuals)[-int(len(residuals) * 0.95)]
                slope_sum += slope
                count += 1

    if count < 4:
        return {
            "metric_name": "slope",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient data"
        }

    mean_slope = slope_sum / count
    mean_residual = residual_sum / count

    return {
        "metric_name": "slope",
        "metric_value": mean_slope,
        "instances_tested": len(results),
        "conjecture_holds": mean_slope <= 3 * phi(m) and mean_residual <= phi(m),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    all_results = [r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]
    support_fraction = len(all_results) / len(results)

    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in all_results)/len(all_results)} std=NA support_fraction={support_fraction}"
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False)
        RESULT = f"FALSIFIED counterexample=\"slope too high\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient data"

    print(RESULT)