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

def generate_3cnf(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def is_satisfiable(clauses, n):
    def backtrack(assignment, clauses):
        if not clauses:
            return True
        clause = clauses[0]
        remaining_clauses = clauses[1:]
        for literal in clause:
            new_assignment = assignment.copy()
            if literal > 0:
                new_assignment[literal] = True
            else:
                new_assignment[-literal] = False
            if all(any(new_assignment.get(abs(lit), False) if lit > 0 else not new_assignment.get(abs(lit), False) for lit in clause) for clause in remaining_clauses):
                if backtrack(new_assignment, remaining_clauses):
                    return True
        return False
    return backtrack({}, clauses)

def dpll_size(clauses, n):
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        clause = clauses[0]
        remaining_clauses = clauses[1:]
        size = 0
        for literal in clause:
            new_assignment = assignment.copy()
            if literal > 0:
                new_assignment[literal] = True
            else:
                new_assignment[-literal] = False
            new_clauses = [c for c in remaining_clauses if not all(any(new_assignment.get(abs(lit), False) if lit > 0 else not new_assignment.get(abs(lit), False) for lit in c))]
            size += dpll(new_clauses, new_assignment)
        return size
    return dpll(clauses, {})

def walsh_hadamard_transform(n, f):
    if n == 0:
        return [f([1]*n)]
    else:
        w = walsh_hadamard_transform(n-1, f)
        return w + [x + y for x, y in zip(w, w)]

def compute_psi_f(clauses, n):
    m = len(clauses)
    inputs = list(itertools.product([-1, 1], repeat=n))
    psi_f = []
    for x in inputs:
        falsified = sum(1 for clause in clauses if not any((lit > 0 and x[abs(lit)-1] == 1) or (lit < 0 and x[abs(lit)-1] == -1) for lit in clause))
        psi_f.append(falsified / m)
    return psi_f

def compute_var_and_stab(psi_f, n):
    rho = 1 - 1/n
    psi_f_hat = walsh_hadamard_transform(n, lambda x: sum(psi_f[i] * math.prod(x[j] for j in range(n)) for i in range(len(psi_f)))) / (2**n)
    var = sum(psi_f_hat[i]**2 for i in range(len(psi_f_hat))) - psi_f_hat[0]**2
    stab = sum((1 - rho**i) * psi_f_hat[i]**2 for i in range(len(psi_f_hat)))
    return var, stab

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    alpha_values = [4.2, 4.6]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            for _ in range(30):
                clauses = generate_3cnf(n, m)
                if not is_satisfiable(clauses, n):
                    psi_f = compute_psi_f(clauses, n)
                    var, stab = compute_var_and_stab(psi_f, n)
                    nsm = (var - stab) / var if var != 0 else 0
                    t_star = dpll_size(clauses, n)
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
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log2(t*(F)) / (n * NSM(F))",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))

    return {
        "metric_name": "log2(t*(F)) / (n * NSM(F))",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")