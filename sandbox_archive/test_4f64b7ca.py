# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_multiply(A, B):
    """Multiply two matrices A and B."""
    if len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions for multiplication")
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    """Transpose a matrix A."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def generate_parity_cnf(n):
    """Generate the canonical PARITY CNF for n inputs."""
    m = 2 ** (n - 1)
    clauses = []
    for i in range(m):
        clause = []
        for j in range(n):
            if (i >> j) & 1:
                clause.append(1)
            else:
                clause.append(-1)
        clauses.append(clause)
    return clauses

def generate_random_ac0_circuit(n, m, w):
    """Generate a random AC0 circuit with m gates and maximum fan-in w."""
    gates = []
    for _ in range(m):
        gate = []
        fan_in = random.randint(1, w)
        inputs = random.sample(range(n), fan_in)
        for j in range(n):
            if j in inputs:
                sign = random.choice([-1, 1])
                gate.append(sign)
            else:
                gate.append(0)
        gates.append(gate)
    return gates

def compute_psi(C, n):
    """Compute the L_infinity discrepancy psi(C)."""
    m = len(C)
    min_max_sum = float('inf')
    for chi in itertools.product([-1, 1], repeat=n):
        max_sum = 0
        for i in range(m):
            row_sum = sum(C[i][j] * chi[j] for j in range(n))
            max_sum = max(max_sum, abs(row_sum))
        if max_sum < min_max_sum:
            min_max_sum = max_sum
    return min_max_sum

def compute_w(C):
    """Compute the maximum bottom fan-in w(C)."""
    return max(sum(1 for x in row if x != 0) for row in C)

def is_parity_circuit(C, n):
    """Check if the circuit computes PARITY_n."""
    for inputs in itertools.product([0, 1], repeat=n):
        output = 0
        for clause in C:
            clause_output = 1
            for j in range(n):
                if clause[j] == 1 and inputs[j] == 0:
                    clause_output = 0
                elif clause[j] == -1 and inputs[j] == 1:
                    clause_output = 0
            output ^= clause_output
        if output != sum(inputs) % 2:
            return False
    return True

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate the canonical PARITY CNF
        C_cnf = generate_parity_cnf(n)
        psi_cnf = compute_psi(C_cnf, n)
        w_cnf = compute_w(C_cnf)
        ratio_cnf = psi_cnf / w_cnf if w_cnf != 0 else 0
        if ratio_cnf < 0.25:
            conjecture_holds = False
            counterexample = f"PARITY CNF with psi/w = {ratio_cnf} < 0.25 for n={n}"
            break

        # Generate a depth-3 PARITY circuit
        if n % 2 == 0:
            C_depth3 = generate_random_ac0_circuit(n, 2 ** (n - 2), n // 2)
            psi_depth3 = compute_psi(C_depth3, n)
            w_depth3 = compute_w(C_depth3)
            ratio_depth3 = psi_depth3 / w_depth3 if w_depth3 != 0 else 0
            if ratio_depth3 < 0.25:
                conjecture_holds = False
                counterexample = f"Depth-3 PARITY circuit with psi/w = {ratio_depth3} < 0.25 for n={n}"
                break

        # Generate random non-PARITY AC0 circuits
        for _ in range(30):
            m = random.randint(1, 2 ** (n - 1))
            w = random.randint(1, n)
            C_random = generate_random_ac0_circuit(n, m, w)
            if is_parity_circuit(C_random, n):
                psi_random = compute_psi(C_random, n)
                w_random = compute_w(C_random)
                ratio_random = psi_random / w_random if w_random != 0 else 0
                if ratio_random < 0.25:
                    conjecture_holds = False
                    counterexample = f"Random PARITY circuit with psi/w = {ratio_random} < 0.25 for n={n}"
                    break

        if not conjecture_holds:
            break

        instances_tested += 1
        metric_values.append(ratio_cnf)

    if conjecture_holds:
        metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    else:
        metric_value = 0

    return {
        "metric_name": "psi/w ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)

    metric_values = [r['metric_value'] for r in results if r['conjecture_holds']]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results) if results else 0
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")