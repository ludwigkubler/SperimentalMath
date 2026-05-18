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
import itertools
from fractions import Fraction

def generate_3cnf(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def evaluate_clause(clause, assignment):
    for lit in clause:
        var = abs(lit)
        val = assignment[var - 1]
        if lit > 0 and val == 1:
            return False
        if lit < 0 and val == -1:
            return False
    return True

def compute_psi_f(clauses, n):
    psi_f = []
    for assignment in itertools.product([-1, 1], repeat=n):
        falsified = sum(1 for clause in clauses if evaluate_clause(clause, assignment))
        psi_f.append(Fraction(falsified, len(clauses)))
    return psi_f

def walsh_hadamard_transform(psi_f, n):
    N = 2 ** n
    psi_hat = [0] * N
    for S in range(N):
        sum_val = Fraction(0, 1)
        for x in range(N):
            product = 1
            for i in range(n):
                if (S >> i) & 1:
                    product *= psi_f[x][i]
            sum_val += product
        psi_hat[S] = sum_val / N
    return psi_hat

def compute_var_and_stab(psi_f, psi_hat, n, rho):
    var = sum(psi ** 2 for psi in psi_f) / (2 ** n) - (sum(psi_f) / (2 ** n)) ** 2
    stab = sum((rho ** bin(S).count('1')) * (psi_hat[S] ** 2) for S in range(1, 2 ** n))
    return var, stab

def compute_nsm(var, stab):
    if var == 0:
        return 0
    return (var - stab) / var

def dpll(clauses, assignment, n):
    if not clauses:
        return True
    for clause in clauses:
        if evaluate_clause(clause, assignment):
            continue
        for lit in clause:
            var = abs(lit)
            if assignment[var - 1] == 0:
                new_assignment = assignment.copy()
                new_assignment[var - 1] = 1 if lit > 0 else -1
                if dpll(clauses, new_assignment, n):
                    return True
    return False

def count_dpll_leaves(clauses, n):
    leaves = 0
    stack = [(clauses, [0] * n)]
    while stack:
        current_clauses, current_assignment = stack.pop()
        if not current_clauses:
            leaves += 1
            continue
        for clause in current_clauses:
            if evaluate_clause(clause, current_assignment):
                continue
            for lit in clause:
                var = abs(lit)
                if current_assignment[var - 1] == 0:
                    new_assignment = current_assignment.copy()
                    new_assignment[var - 1] = 1 if lit > 0 else -1
                    stack.append((current_clauses, new_assignment))
                    break
    return leaves

def run_trial(seed):
    n_values = [10, 12, 14, 16]
    alpha_values = [4.2, 4.6]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            clauses = generate_3cnf(n, alpha, seed)
            assignment = [0] * n
            if not dpll(clauses, assignment, n):
                psi_f = compute_psi_f(clauses, n)
                psi_hat = walsh_hadamard_transform(psi_f, n)
                var, stab = compute_var_and_stab(psi_f, psi_hat, n, 1 - 1/n)
                nsm = compute_nsm(var, stab)
                t_star = count_dpll_leaves(clauses, n)
                metric_value = math.log2(t_star) / (n * nsm) if nsm != 0 else 0
                metric_values.append(metric_value)
                instances_tested += 1
                if metric_value < 1/16:
                    conjecture_holds = False
                    counterexample = f"n={n}, alpha={alpha}, clauses={clauses}"
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "log2(t*) / (n * NSM)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsat instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(t*) / (n * NSM)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_unsat_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")