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

def generate_random_ac0_circuit(n, max_gates):
    circuit = []
    for _ in range(random.randint(1, max_gates)):
        gate_type = random.choice(['NOT', 'XOR'])
        if gate_type == 'NOT':
            gate = (gate_type, random.randint(0, n-1))
        else:
            gate = (gate_type, random.sample(range(n), 2))
        circuit.append(gate)
    return circuit

def construct_non_associative_algebra(circuit):
    n = len(circuit)
    algebra = [[0] * n for _ in range(n)]
    for i in range(n):
        algebra[i][i] = 1
    for gate in circuit:
        if gate[0] == 'NOT':
            qubit = gate[1]
            for j in range(n):
                algebra[qubit][j], algebra[j][qubit] = algebra[j][qubit], algebra[qubit][j]
        else:
            qubits = gate[1]
            for j in range(n):
                if j not in qubits:
                    algebra[qubits[0]][j], algebra[j][qubits[0]] = algebra[j][qubits[0]], algebra[qubits[0]][j]
                    algebra[qubits[1]][j], algebra[j][qubits[1]] = algebra[j][qubits[1]], algebra[qubits[1]][j]
    return algebra

def calculate_symplectic_form(algebra):
    n = len(algebra)
    symplectic_form = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                symplectic_form[i][j] = algebra[i][j] * algebra[j][i]
    return symplectic_form

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    max_gates = 40
    circuit = generate_random_ac0_circuit(n, max_gates)
    algebra = construct_non_associative_algebra(circuit)
    symplectic_form = calculate_symplectic_form(algebra)
    gate_count = len(circuit)
    metric_value = sum(sum(row) for row in symplectic_form) / (n * n)
    conjecture_holds = abs(gate_count - metric_value) < 1e-6
    counterexample = "" if conjecture_holds else f"Gate count {gate_count} does not match symplectic form rank {metric_value}"
    return {
        "metric_name": "Symplectic Form Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")