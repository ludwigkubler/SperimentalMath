# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from fractions import Fraction
from itertools import product

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        signs = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append(list(zip(clause, signs)))
    return clauses

def evaluate_clause(clause, assignment):
    for var, sign in clause:
        if assignment[var] == sign:
            return False
    return True

def psi_f(clauses, assignment):
    falsified = sum(1 for clause in clauses if evaluate_clause(clause, assignment))
    return Fraction(falsified, len(clauses))

def walsh_hadamard_transform(psi_values, n):
    size = 2 ** n
    psi_hat = [Fraction(0, 1) for _ in range(size)]
    for x in range(size):
        assignment = [(-1) ** ((x >> i) & 1) for i in range(n)]
        psi_hat[x] = psi_values[x]
    for i in range(n):
        for j in range(size):
            if (j >> i) & 1:
                psi_hat[j] += psi_hat[j ^ (1 << i)]
            else:
                psi_hat[j] -= psi_hat[j ^ (1 << i)]
    for j in range(size):
        psi_hat[j] /= size
    return psi_hat

def compute_nsm(psi_hat, n):
    rho = 1 - Fraction(1, n)
    var_psi = sum(psi_hat[s] ** 2 for s in range(1, len(psi_hat)))
    stab_rho = sum((rho ** len(bin(s)[2:])) * psi_hat[s] ** 2 for s in range(1, len(psi_hat)))
    if var_psi == 0:
        return 0
    nsm = (var_psi - stab_rho) / var_psi
    return float(nsm)

def dpll(clauses, assignment, n):
    if not clauses:
        return 1
    for clause in clauses:
        if evaluate_clause(clause, assignment):
            continue
        for var, sign in clause:
            new_assignment = assignment.copy()
            new_assignment[var] = sign
            new_clauses = [c for c in clauses if not evaluate_clause(c, new_assignment)]
            result = dpll(new_clauses, new_assignment, n)
            if result != 0:
                return result + 1
        return 0
    return 1

def run_trial(seed):
    n = random.choice([10, 12, 14, 16])
    alpha = random.choice([4.2, 4.6])
    m = int(alpha * n)
    clauses = generate_3cnf(n, m, seed)
    psi_values = []
    for x in range(2 ** n):
        assignment = [(-1) ** ((x >> i) & 1) for i in range(n)]
        psi_values.append(psi_f(clauses, assignment))
    psi_hat = walsh_hadamard_transform(psi_values, n)
    nsm = compute_nsm(psi_hat, n)
    t_star = dpll(clauses, [0] * n, n)
    if t_star == 0:
        return {
            "metric_name": "log_2 t*(F)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    log_t_star = math.log2(t_star)
    margin = log_t_star - (n * nsm / 16)
    conjecture_holds = margin >= 0
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, NSM={nsm}, t*={t_star}"
    return {
        "metric_name": "log_2 t*(F)",
        "metric_value": log_t_star,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    metric_values = [trial["metric_value"] for trial in results if trial["metric_value"] != 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexample = next((trial["counterexample"] for trial in results if not trial["conjecture_holds"]), "")
        first_failing_seed = next((trial["seed"] for trial in results if not trial["conjecture_holds"]), -1)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")