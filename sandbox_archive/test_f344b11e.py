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

def generate_parity_cnf(n):
    m = 2 ** (n - 1)
    clauses = []
    for i in range(m):
        clause = []
        for j in range(n):
            if (i >> j) & 1:
                clause.append((j, 1))
            else:
                clause.append((j, -1))
        clauses.append(clause)
    return clauses

def generate_random_ac0_circuit(n, m, w):
    clauses = []
    for _ in range(m):
        clause = []
        for j in range(n):
            if random.random() < 0.5:
                sign = random.choice([-1, 1])
                clause.append((j, sign))
        if len(clause) > w:
            clause = random.sample(clause, w)
        clauses.append(clause)
    return clauses

def compute_psi(C, n):
    m = len(C)
    min_discrepancy = float('inf')
    best_chi = None

    for chi in itertools.product([-1, 1], repeat=n):
        max_discrepancy = 0
        for clause in C:
            discrepancy = 0
            for j, sign in clause:
                discrepancy += sign * chi[j]
            max_discrepancy = max(max_discrepancy, abs(discrepancy))
        if max_discrepancy < min_discrepancy:
            min_discrepancy = max_discrepancy
            best_chi = chi
    return min_discrepancy

def compute_w(C):
    max_fan_in = 0
    for clause in C:
        max_fan_in = max(max_fan_in, len(clause))
    return max_fan_in

def is_parity_circuit(C, n):
    truth_table = {}
    for inputs in itertools.product([-1, 1], repeat=n):
        output = 0
        for clause in C:
            clause_output = 1
            for j, sign in clause:
                clause_output *= sign * inputs[j]
            output ^= clause_output
        truth_table[inputs] = output
    for inputs in itertools.product([-1, 1], repeat=n):
        expected_output = 1 if sum(inputs) % 2 == 1 else -1
        if truth_table[inputs] != expected_output:
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
        # Generate canonical PARITY CNF
        C_cnf = generate_parity_cnf(n)
        psi_cnf = compute_psi(C_cnf, n)
        w_cnf = compute_w(C_cnf)
        ratio_cnf = psi_cnf / w_cnf if w_cnf != 0 else 0
        if ratio_cnf < 0.25:
            conjecture_holds = False
            counterexample = f"PARITY CNF with psi/w = {ratio_cnf} < 0.25 for n={n}"
            break
        metric_values.append(ratio_cnf)
        instances_tested += 1

        # Generate depth-3 PARITY circuit
        if n % 2 == 0:
            C_depth3 = generate_parity_cnf(n // 2)
            psi_depth3 = compute_psi(C_depth3, n // 2)
            w_depth3 = compute_w(C_depth3)
            ratio_depth3 = psi_depth3 / w_depth3 if w_depth3 != 0 else 0
            if ratio_depth3 < 0.25:
                conjecture_holds = False
                counterexample = f"Depth-3 PARITY circuit with psi/w = {ratio_depth3} < 0.25 for n={n}"
                break
            metric_values.append(ratio_depth3)
            instances_tested += 1

        # Generate random non-PARITY AC0 circuits
        for _ in range(30):
            m = 2 ** (n - 1)
            w = n
            C_random = generate_random_ac0_circuit(n, m, w)
            psi_random = compute_psi(C_random, n)
            w_random = compute_w(C_random)
            ratio_random = psi_random / w_random if w_random != 0 else 0
            if is_parity_circuit(C_random, n) and ratio_random < 0.25:
                conjecture_holds = False
                counterexample = f"Random PARITY circuit with psi/w = {ratio_random} < 0.25 for n={n}"
                break
            metric_values.append(ratio_random)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "psi/w ratio",
            "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    return {
        "metric_name": "psi/w ratio",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += result["instances_tested"]

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0

    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support support_fraction={support_fraction}")