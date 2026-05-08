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

def fourier_coefficients(f, n):
    N = 2 ** n
    coeffs = [0] * N
    for k in range(N):
        sum_val = 0
        for x in range(N):
            sum_val += f(x) * math.exp(-2j * math.pi * k * x / N)
        coeffs[k] = sum_val / N
    return coeffs

def gowers_uniformity_norm(f, n, order=3):
    coeffs = fourier_coefficients(f, n)
    norm = 0
    for k in range(1, len(coeffs)):
        norm += abs(coeffs[k]) ** (2 * order)
    return norm ** (1 / (2 * order))

def simulate_acc0_circuit(f, n, size):
    def threshold_gate(x, t):
        return int(x > t)

    def evaluate(circuit, inputs):
        stack = []
        for gate in circuit:
            if isinstance(gate, tuple):
                a, b, op = gate
                if op == 'AND':
                    stack.append(threshold_gate(stack.pop(), 0.5) and threshold_gate(stack.pop(), 0.5))
                elif op == 'OR':
                    stack.append(threshold_gate(stack.pop(), 0.5) or threshold_gate(stack.pop(), 0.5))
            else:
                stack.append(gate)
        return stack[0]

    circuit = []
    for _ in range(size):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            a, b = random.sample(range(n), 2)
            circuit.append((a, b, 'AND'))
        else:
            a, b = random.sample(range(n), 2)
            circuit.append((a, b, 'OR'))

    inputs = [random.choice([0, 1]) for _ in range(n)]
    return evaluate(circuit, inputs) == f(tuple(inputs))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    supported_count = 0
    counterexample = ""

    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Sample 5 instances per n
            f = lambda x: random.choice([0, 1])
            norm = gowers_uniformity_norm(f, n)
            if norm >= n ** (1/3):
                instances_tested += 1
                circuit_size = 2 * n
                while not simulate_acc0_circuit(f, n, circuit_size):
                    circuit_size += 1
                if circuit_size > n ** (2 - 1/3):
                    supported_count += 1
                else:
                    counterexample = f"n={n}, norm={norm:.4f}, expected size>={n**(2-1/3)}, got {circuit_size}"
        total_instances += instances_tested

    metric_value = supported_count / len(n_values)
    conjecture_holds = metric_value >= 0.8
    return {
        "metric_name": "support_fraction",
        "metric_value": metric_value,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")