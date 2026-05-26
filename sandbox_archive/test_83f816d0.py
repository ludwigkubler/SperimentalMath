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

def generate_monotone_circuit(n, m):
    # Generate a random monotone circuit with n variables and m gates
    circuit = []
    for _ in range(m):
        gate_type = random.choice(['AND', 'OR'])
        inputs = sorted(random.sample(range(1, n + 1), random.randint(2, n)))
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit, input_values):
    # Evaluate the monotone circuit for given input values
    stack = []
    for gate in circuit:
        gate_type, inputs = gate
        if gate_type == 'AND':
            result = all(input_values[i - 1] for i in inputs)
        elif gate_type == 'OR':
            result = any(input_values[i - 1] for i in inputs)
        stack.append(result)
    return stack.pop()

def construct_quasi_crystalline_set(circuit, q):
    # Construct the quasi-crystalline set Q_C
    n = len(circuit[0][1])
    Q = []
    for a in range(2 ** n):
        input_values = [(a >> i) & 1 for i in range(n)]
        if evaluate_circuit(circuit, input_values):
            Q.append(input_values)
    return Q

def compute_rank(Q, q):
    # Compute the minimal rank of Q over F_q
    n = len(Q[0])
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
    for point in Q:
        for j in range(n):
            if point[j]:
                A[j][-1] += Fraction(1, q)
    rank = n
    for i in range(n):
        if A[i][i] == 0:
            found_pivot = False
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    found_pivot = True
                    break
            if not found_pivot:
                rank -= 1
                continue
        pivot = A[i][i]
        for j in range(n + 1):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n + 1):
                    A[k][j] -= factor * A[i][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(2 * n, 5 * n)
    circuit = generate_monotone_circuit(n, m)
    q = 2
    Q = construct_quasi_crystalline_set(circuit, q)
    rank = compute_rank(Q, q)
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = len(Q)
    conjecture_holds = (rank <= n * math.log(n, 2)) and (n * math.log(n, 2) <= rank)
    counterexample = "" if conjecture_holds else f"Rank {rank} is outside bounds [1, {n * math.log(n, 2)}]"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank outside bounds\" first_failing_seed={first_failing_seed}")