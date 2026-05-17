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
                clause.append((j, +1))
            else:
                clause.append((j, -1))
        clauses.append(clause)
    return clauses

def generate_random_ac0_circuit(n, m, w):
    clauses = []
    for _ in range(m):
        clause = []
        literals = random.sample(range(n), random.randint(1, w))
        for j in literals:
            clause.append((j, random.choice([-1, +1])))
        clauses.append(clause)
    return clauses

def compute_psi(C, n):
    m = len(C)
    min_max_sum = float('inf')
    for chi in itertools.product([-1, +1], repeat=n):
        max_sum = 0
        for clause in C:
            sum_val = 0
            for j, sign in clause:
                sum_val += sign * chi[j]
            max_sum = max(max_sum, abs(sum_val))
        min_max_sum = min(min_max_sum, max_sum)
    return min_max_sum

def compute_w(C):
    max_fan_in = 0
    for clause in C:
        max_fan_in = max(max_fan_in, len(clause))
    return max_fan_in

def is_parity_circuit(C, n):
    truth_table = {}
    for inputs in itertools.product([-1, +1], repeat=n):
        output = 0
        for clause in C:
            clause_val = 1
            for j, sign in clause:
                clause_val *= sign * inputs[j]
            output += clause_val
        output = output % 2
        truth_table[inputs] = output
    for inputs in itertools.product([-1, +1], repeat=n):
        expected = sum(inputs) % 2
        if truth_table[inputs] != expected:
            return False
    return True

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    results = []
    for n in n_values:
        # Generate canonical PARITY CNF
        C_cnf = generate_parity_cnf(n)
        psi_cnf = compute_psi(C_cnf, n)
        w_cnf = compute_w(C_cnf)
        ratio_cnf = psi_cnf / w_cnf if w_cnf != 0 else 0
        is_parity_cnf = is_parity_circuit(C_cnf, n)

        # Generate depth-3 PARITY circuit
        m_depth3 = 2 ** (n - 2)
        w_depth3 = n // 2 + 1
        C_depth3 = generate_random_ac0_circuit(n, m_depth3, w_depth3)
        psi_depth3 = compute_psi(C_depth3, n)
        w_depth3 = compute_w(C_depth3)
        ratio_depth3 = psi_depth3 / w_depth3 if w_depth3 != 0 else 0
        is_parity_depth3 = is_parity_circuit(C_depth3, n)

        # Generate random non-PARITY circuits
        m_random = 2 ** (n - 1)
        w_random = n
        C_random = generate_random_ac0_circuit(n, m_random, w_random)
        psi_random = compute_psi(C_random, n)
        w_random = compute_w(C_random)
        ratio_random = psi_random / w_random if w_random != 0 else 0
        is_parity_random = is_parity_circuit(C_random, n)

        results.append({
            "n": n,
            "psi_cnf": psi_cnf,
            "w_cnf": w_cnf,
            "ratio_cnf": ratio_cnf,
            "is_parity_cnf": is_parity_cnf,
            "psi_depth3": psi_depth3,
            "w_depth3": w_depth3,
            "ratio_depth3": ratio_depth3,
            "is_parity_depth3": is_parity_depth3,
            "psi_random": psi_random,
            "w_random": w_random,
            "ratio_random": ratio_random,
            "is_parity_random": is_parity_random
        })

    # Compute overall metrics
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    for result in results:
        if result["is_parity_cnf"] and result["ratio_cnf"] < 0.25:
            conjecture_holds = False
            counterexample = f"PARITY CNF with n={result['n']} has ratio {result['ratio_cnf']} < 0.25"
            break
        if result["is_parity_depth3"] and result["ratio_depth3"] < 0.25:
            conjecture_holds = False
            counterexample = f"Depth-3 PARITY circuit with n={result['n']} has ratio {result['ratio_depth3']} < 0.25"
            break
        metric_values.append(result["ratio_cnf"])

    if conjecture_holds:
        for result in results:
            if result["is_parity_cnf"]:
                metric_values.append(result["ratio_cnf"])

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0

    return {
        "metric_name": "psi/w ratio",
        "metric_value": metric_value,
        "instances_tested": len(results) * 3,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        trials.append(result)

    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))

    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((trial["seed"] for trial in trials if not trial["conjecture_holds"]), None)
        counterexample = next((trial["counterexample"] for trial in trials if not trial["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")