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

def build_flat_dnf(n):
    gates = []
    for i in range(2 ** (n - 1)):
        term = []
        for j in range(n):
            if (i >> j) & 1:
                term.append(('input', j))
        gates.append(('AND', term))
    or_gate = ('OR', gates)
    return or_gate

def build_xor_tree(n):
    if n == 1:
        return ('input', 0)
    left = build_xor_tree(n // 2)
    right = build_xor_tree((n + 1) // 2)
    return ('XOR', [left, right])

def demorgan_expand(gate):
    op, children = gate
    if op == 'XOR':
        a, b = children
        a_not = ('NOT', [a])
        b_not = ('NOT', [b])
        and1 = ('AND', [a, b_not])
        and2 = ('AND', [a_not, b])
        return ('OR', [and1, and2])
    elif op == 'NOT':
        child = children[0]
        if child[0] == 'AND':
            new_children = [('NOT', [c]) for c in child[1]]
            return ('OR', new_children)
        elif child[0] == 'OR':
            new_children = [('NOT', [c]) for c in child[1]]
            return ('AND', new_children)
        elif child[0] == 'NOT':
            return child[1][0]
    return gate

def build_block_parity(n, block_size):
    if n <= block_size:
        return build_xor_tree(n)
    blocks = []
    for i in range(0, n, block_size):
        blocks.append(build_xor_tree(min(block_size, n - i)))
    return build_xor_tree(len(blocks))

def build_random_circuit(n, depth):
    if depth == 1:
        return ('input', random.randint(0, n - 1))
    ops = ['AND', 'OR', 'NOT']
    op = random.choice(ops)
    if op == 'NOT':
        child = build_random_circuit(n, depth - 1)
        return ('NOT', [child])
    else:
        num_children = random.randint(2, 3)
        children = [build_random_circuit(n, depth - 1) for _ in range(num_children)]
        return (op, children)

def compute_size(gate):
    op, children = gate
    if op == 'input':
        return 1
    return 1 + sum(compute_size(child) for child in children)

def compute_depth(gate):
    op, children = gate
    if op == 'input':
        return 1
    return 1 + max(compute_depth(child) for child in children)

def hash_gate(gate):
    op, children = gate
    if op == 'input':
        return hash((op, children[0]))
    child_hashes = sorted(hash_gate(child) for child in children)
    return hash((op, tuple(child_hashes)))

def apply_shift(gate, shift, n):
    op, children = gate
    if op == 'input':
        return ('input', (children[0] + shift) % n)
    new_children = [apply_shift(child, shift, n) for child in children]
    return (op, new_children)

def canonical_form(gate, n):
    op, children = gate
    if op == 'input':
        return gate
    min_form = gate
    for shift in range(n):
        shifted = apply_shift(gate, shift, n)
        if shifted < min_form:
            min_form = shifted
    return min_form

def compute_psi(gate, n):
    gate_hash = hash_gate(gate)
    canonical = canonical_form(gate, n)
    canonical_hash = hash_gate(canonical)
    orbits = defaultdict(list)
    orbits[canonical_hash].append(gate_hash)
    for child in gate[1]:
        child_orbits = compute_psi(child, n)
        for key, value in child_orbits.items():
            orbits[key].extend(value)
    return orbits

def run_trial(seed):
    random.seed(seed)
    n = random.choice([3, 5, 7, 11, 13, 17, 19, 23])
    depth = random.choice([2, 3, 4])
    construction = random.choice(['flat_dnf', 'xor_tree', 'block_parity', 'random'])

    if construction == 'flat_dnf':
        circuit = build_flat_dnf(n)
    elif construction == 'xor_tree':
        circuit = build_xor_tree(n)
        circuit = demorgan_expand(circuit)
    elif construction == 'block_parity':
        block_size = random.randint(2, n // 2)
        circuit = build_block_parity(n, block_size)
        circuit = demorgan_expand(circuit)
    else:
        circuit = build_random_circuit(n, depth)

    s = compute_size(circuit)
    d = compute_depth(circuit)
    orbits = compute_psi(circuit, n)
    psi = len(orbits)

    if s == 0:
        r = 0.0
    else:
        r = (4 * d * psi) / math.log2(s)

    is_parity = construction in ['flat_dnf', 'xor_tree', 'block_parity']
    conjecture_holds = r >= 1 if is_parity else True

    counterexample = ""
    if is_parity and not conjecture_holds:
        counterexample = f"n={n}, depth={depth}, construction={construction}, r={r}"

    return {
        "metric_name": "4dψ/log2(s)",
        "metric_value": r,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(2, 100)[:30]

    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")