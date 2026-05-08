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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
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
    
    def xor_tree(n, depth):
        if n == 1:
            return [set([i]) for i in range(depth)]
        else:
            left = xor_tree(n // 2, depth)
            right = xor_tree(n - n // 2, depth)
            return [left[i] | right[i] for i in range(len(left))] + [left[i] & right[i] for i in range(len(left))]
    
    def is_parity_circuit(circuit):
        truth_table = {}
        for x in range(1 << len(circuit)):
            inputs = [(x >> i) & 1 for i in range(len(circuit))]
            output = 0
            for gate in circuit:
                if len(gate) == 2 and gate[1] == 'XOR':
                    output ^= inputs[gate[0]]
                elif len(gate) == 3 and gate[1] == 'AND':
                    output &= inputs[gate[0]] & inputs[gate[2]]
                elif len(gate) == 3 and gate[1] == 'OR':
                    output |= inputs[gate[0]] | inputs[gate[2]]
            truth_table[x] = output
        return all(truth_table[x] == (x & 1) for x in range(1 << len(circuit)))
    
    def meet_closure(supports):
        closure = set()
        stack = list(supports)
        while stack:
            s = stack.pop()
            if s not in closure:
                closure.add(s)
                for t in supports:
                    if s.issubset(t) and t not in closure:
                        stack.append(t)
        return closure
    
    def mobius_function(lattice):
        n = len(lattice)
        mu = [[0] * n for _ in range(n)]
        mu[0][0] = 1
        for i in range(1, n):
            for j in range(i, -1, -1):
                if lattice[j].issubset(lattice[i]):
                    mu[i][j] = sum(mu[j][k] for k in range(j + 1, i + 1))
        return mu
    
    def psi(circuit):
        n = len(circuit)
        depth = max(len(gate) for gate in circuit if len(gate) > 2)
        supports = xor_tree(n, depth)
        lattice = meet_closure(supports)
        mu = mobius_function(lattice)
        return math.log2(1 + sum(abs(mu[0][i]) for i in range(1, len(lattice))))
    
    def canonical_parity_circuit(n):
        circuit = []
        for i in range(n - 1):
            circuit.append((i, 'XOR'))
        circuit.append((n - 1, 'AND', n - 2))
        return circuit
    
    def random_parity_circuit(n):
        circuit = canonical_parity_circuit(n)
        for _ in range(30):
            i = random.randint(0, len(circuit) - 1)
            if circuit[i][1] == 'XOR':
                circuit[i] = (circuit[i][0], 'AND', random.randint(0, n - 2))
            else:
                circuit[i] = (circuit[i][0], 'XOR')
        return circuit
    
    def verify_parity(circuit):
        for x in range(1 << len(circuit)):
            inputs = [(x >> i) & 1 for i in range(len(circuit))]
            output = 0
            for gate in circuit:
                if len(gate) == 2 and gate[1] == 'XOR':
                    output ^= inputs[gate[0]]
                elif len(gate) == 3 and gate[1] == 'AND':
                    output &= inputs[gate[0]] & inputs[gate[2]]
                elif len(gate) == 3 and gate[1] == 'OR':
                    output |= inputs[gate[0]] | inputs[gate[2]]
            if output != (x & 1):
                return False
        return True
    
    def random_gate_merge(circuit):
        i = random.randint(0, len(circuit) - 1)
        j = random.randint(i + 1, len(circuit))
        new_gate = (i, 'XOR', j)
        circuit[i] = new_gate
        del circuit[j]
        return circuit
    
    def dummy_fan_in(circuit):
        i = random.randint(0, len(circuit) - 1)
        if circuit[i][1] == 'XOR':
            circuit[i] = (circuit[i][0], 'AND', random.randint(0, len(circuit) - 2))
        else:
            circuit[i] = (circuit[i][0], 'XOR')
        return circuit
    
    n_values = [4, 8, 12, 16, 20, 24, 32, 40]
    d_values = [2, 3, 4]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for d in d_values:
            canonical_circuit = canonical_parity_circuit(n)
            if is_parity_circuit(canonical_circuit):
                instances_tested += 1
                psi_value = psi(canonical_circuit)
                if psi_value < 0.05 * n ** (1 / (d - 1)):
                    conjecture_holds = False
                    counterexample = f"Canonical circuit with ψ(C)={psi_value} for n={n}, d={d}"
            for _ in range(30):
                random_circuit = random_parity_circuit(n)
                if verify_parity(random_circuit):
                    instances_tested += 1
                    psi_value = psi(random_circuit)
                    if psi_value < 0.05 * n ** (1 / (d - 1)):
                        conjecture_holds = False
                        counterexample = f"Random circuit with ψ(C)={psi_value} for n={n}, d={d}"
    
    return {
        "metric_name": "ψ(C)",
        "metric_value": psi(canonical_parity_circuit(4)),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_psi = sum(r["metric_value"] for r in results) / len(results)
    std_psi = math.sqrt(sum((r["metric_value"] - mean_psi) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_psi} std={std_psi} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")