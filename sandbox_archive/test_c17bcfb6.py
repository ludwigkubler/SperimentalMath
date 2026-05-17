# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(start, end):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def matrix_mult(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_pow(mat, power):
    result = [[1 if i == j else 0 for j in range(len(mat))] for i in range(len(mat))]
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult(result, mat)
        mat = matrix_mult(mat, mat)
        power //= 2
    return result

def build_flat_dnf(n):
    gates = []
    for i in range(2 ** (n - 1)):
        term = []
        for j in range(n):
            if (i >> j) & 1:
                term.append(('NOT', j))
            else:
                term.append(('ID', j))
        gates.append(('AND', term))
    for _ in range(n - 1):
        new_gates = []
        for i in range(0, len(gates), 2):
            if i + 1 < len(gates):
                new_gates.append(('OR', [gates[i], gates[i + 1]]))
            else:
                new_gates.append(gates[i])
        gates = new_gates
    return gates[0]

def build_balanced_xor_tree(n):
    gates = [('ID', i) for i in range(n)]
    while len(gates) > 1:
        new_gates = []
        for i in range(0, len(gates), 2):
            if i + 1 < len(gates):
                new_gates.append(('XOR', [gates[i], gates[i + 1]]))
            else:
                new_gates.append(gates[i])
        gates = new_gates
    return gates[0]

def build_hastad_block_parity(n, block_size):
    gates = []
    for i in range(0, n, block_size):
        block = [('ID', j) for j in range(i, min(i + block_size, n))]
        if len(block) > 1:
            block_gate = ('XOR', block)
            gates.append(block_gate)
        else:
            gates.append(block[0])
    while len(gates) > 1:
        new_gates = []
        for i in range(0, len(gates), 2):
            if i + 1 < len(gates):
                new_gates.append(('XOR', [gates[i], gates[i + 1]]))
            else:
                new_gates.append(gates[i])
        gates = new_gates
    return gates[0]

def build_random_non_parity(n, depth):
    gates = [('ID', i) for i in range(n)]
    for _ in range(depth):
        new_gates = []
        for _ in range(len(gates)):
            op = random.choice(['AND', 'OR', 'XOR', 'NOT'])
            if op == 'NOT':
                gate = (op, [random.choice(gates)])
            else:
                gate = (op, random.sample(gates, 2))
            new_gates.append(gate)
        gates = new_gates
    return random.choice(gates)

def compute_psi(circuit, n):
    gate_hashes = {}
    canonical_forms = {}

    def hash_gate(gate):
        if isinstance(gate, tuple):
            op, children = gate
            if op == 'ID':
                return hash((op, children))
            child_hashes = sorted([hash_gate(child) for child in children])
            return hash((op, tuple(child_hashes)))
        else:
            return hash(gate)

    def get_canonical_form(gate, shift):
        if isinstance(gate, tuple):
            op, children = gate
            if op == 'ID':
                return (op, (shift + children) % n)
            child_forms = sorted([get_canonical_form(child, shift) for child in children])
            return (op, tuple(child_forms))
        else:
            return (('ID', (shift + gate) % n))

    for gate in circuit:
        gate_hashes[gate] = hash_gate(gate)

    for gate in circuit:
        min_form = None
        for shift in range(n):
            form = get_canonical_form(gate, shift)
            if min_form is None or form < min_form:
                min_form = form
        key = tuple(min_form)
        if key not in canonical_forms:
            canonical_forms[key] = []
        canonical_forms[key].append(gate)

    psi = len(canonical_forms)
    return psi

def compute_size(circuit):
    size = 0
    for gate in circuit:
        if isinstance(gate, tuple):
            size += 1 + compute_size(gate[1])
        else:
            size += 1
    return size

def run_trial(seed):
    random.seed(seed)
    n = random.choice([3, 5, 7, 11, 13, 17, 19, 23])
    depth = random.choice([2, 3, 4])
    construction = random.choice(['flat_dnf', 'balanced_xor', 'hastad', 'random_non_parity'])

    if construction == 'flat_dnf':
        circuit = build_flat_dnf(n)
    elif construction == 'balanced_xor':
        circuit = build_balanced_xor_tree(n)
    elif construction == 'hastad':
        block_size = random.randint(2, n // 2)
        circuit = build_hastad_block_parity(n, block_size)
    else:
        circuit = build_random_non_parity(n, depth)

    psi = compute_psi(circuit, n)
    s = compute_size(circuit)
    d = depth

    if s == 0:
        return {
            "metric_name": "psi_ratio",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    r = (4 * d * psi) / math.log2(s)

    if construction == 'random_non_parity':
        return {
            "metric_name": "psi_ratio",
            "metric_value": r,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    if r < 1:
        return {
            "metric_name": "psi_ratio",
            "metric_value": r,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, depth={d}, construction={construction}, r={r}"
        }
    else:
        return {
            "metric_name": "psi_ratio",
            "metric_value": r,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(100, 130)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    holds = [r["conjecture_holds"] for r in results]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_trials")
    else:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(holds) / len(holds)

        if all(holds):
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")