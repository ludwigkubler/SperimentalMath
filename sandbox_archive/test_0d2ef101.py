# auto-injected by SEC sandbox
import itertools
import collections
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
import json
from sys import argv

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    d = 2
    while n >= d * d:
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

def generate_truth_table(n):
    return [random.randint(0, 1) for _ in range(2 ** n)]

def generate_acc_circuit(m, s, n):
    circuit = []
    for _ in range(s):
        gate = random.choice(['AND', 'NOT'])
        if gate == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, int(math.log2(n)) + 1))]
        circuit.append((gate, inputs))
    return circuit

def evaluate_circuit(circuit, input_vector):
    stack = []
    for gate, inputs in reversed(circuit):
        if gate == 'NOT':
            stack.append(not input_vector[inputs[0]])
        else:
            result = input_vector[inputs[0]]
            for i in range(1, len(inputs)):
                if gate == 'AND':
                    result &= input_vector[inputs[i]]
                elif gate == 'OR':
                    result |= input_vector[inputs[i]]
            stack.append(result)
    return stack.pop()

def compute_alpha_f(truth_table, m):
    n = int(math.log2(len(truth_table)))
    alpha_f = 0
    for x in range(2 ** n):
        k = sum(x & (1 << i) for i in range(n))
        alpha_f += truth_table[x] * (complex(math.cos(2 * math.pi * k / m), math.sin(2 * math.pi * k / m)))
    return alpha_f / (2 ** n)

def compute_cyclotomic_norm(alpha_f, m):
    n = int(math.log2(len(truth_table)))
    reg_rep_matrix = []
    for x in range(m):
        row = [complex(math.cos(2 * math.pi * i * x / m), math.sin(2 * math.pi * i * x / m)) for i in range(n)]
        reg_rep_matrix.append(row)
    det = 1
    for i in range(n):
        det *= reg_rep_matrix[i][i]
    return abs(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [6, 10, 15]
    n_values = [8, 10, 12, 14]
    s_values = [4, 8, 16, 32, 64]
    num_trials = 400
    controls = 200

    results = []
    for m in m_values:
        if len(prime_factors(m)) < 2:
            continue
        for n in n_values:
            for s in s_values:
                for _ in range(num_trials):
                    circuit = generate_acc_circuit(m, s, n)
                    truth_table = generate_truth_table(n)
                    alpha_f = compute_alpha_f(truth_table, m)
                    norm = compute_cyclotomic_norm(alpha_f, m)
                    results.append(-math.log2(norm), math.log2(s))

    for _ in range(controls):
        truth_table = generate_truth_table(random.randint(8, 14))
        alpha_f = compute_alpha_f(truth_table, random.choice([6, 10, 15]))
        norm = compute_cyclotomic_norm(alpha_f, random.choice([6, 10, 15]))
        results.append(-math.log2(norm), math.log2(2 ** random.randint(8, 14)))

    for _ in range(controls):
        n = random.randint(8, 14)
        alpha_f = compute_alpha_f([random.randint(0, 1) for _ in range(2 ** n)], random.choice([6, 10, 15]))
        norm = compute_cyclotomic_norm(alpha_f, random.choice([6, 10, 15]))
        results.append(-math.log2(norm), math.log2(2 ** n))

    slope, intercept = 0, 0
    for y, x in results:
        slope += (y - intercept) * x / len(results)
        intercept += (y - intercept) * (1 - x) / len(results)

    mean_slope = sum(y - intercept for y, _ in results) / len(results)
    std_slope = math.sqrt(sum((y - intercept - mean_slope) ** 2 for y, _ in results) / len(results))
    mean_resid = sum(abs(y - (intercept + slope * x)) for y, x in results) / len(results)
    std_resid = math.sqrt(sum((abs(y - (intercept + slope * x)) - mean_resid) ** 2 for y, x in results) / len(results))

    conjecture_holds = all(slope <= 3 * phi(m) and mean_resid <= phi(m) for m in m_values for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "slope",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in argv[1:]] if argv[1:] else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_slope = sum(r["metric_value"] for r in results) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 100 * phi(m) * math.log2(s) for m, n, s in [(6, 8, 4), (6, 8, 8), (6, 8, 16), (6, 8, 32), (6, 8, 64), (10, 8, 4), (10, 8, 8), (10, 8, 16), (10, 8, 32), (10, 8, 64), (15, 8, 4), (15, 8, 8), (15, 8, 16), (15, 8, 32), (15, 8, 64)]):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")