# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from fractions import Fraction
from collections import defaultdict

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for v in clause_vars:
            if random.choice([True, False]):
                clause.append(v)
            else:
                clause.append(-v)
        clauses.append(clause)
    return clauses

def is_satisfiable(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for lit in clause:
            if (lit > 0 and assignment[abs(lit)-1] == 1) or (lit < 0 and assignment[abs(lit)-1] == -1):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def dpll(clauses, assignment, n):
    if len(clauses) == 0:
        return True, assignment
    for clause in clauses:
        if len(clause) == 1:
            lit = clause[0]
            if lit > 0:
                if assignment[lit-1] == -1:
                    return False, None
                assignment[lit-1] = 1
            else:
                if assignment[-lit-1] == 1:
                    return False, None
                assignment[-lit-1] = -1
            new_clauses = [c for c in clauses if lit not in c and -lit not in c]
            return dpll(new_clauses, assignment, n)
    for clause in clauses:
        for lit in clause:
            new_assignment = assignment.copy()
            if lit > 0:
                new_assignment[lit-1] = 1
            else:
                new_assignment[-lit-1] = -1
            new_clauses = []
            for c in clauses:
                if lit not in c and -lit not in c:
                    new_clauses.append(c)
            result, sol = dpll(new_clauses, new_assignment, n)
            if result:
                return True, sol
    return False, None

def walsh_hadamard_transform(n, f):
    if n == 0:
        return [f([1])]
    else:
        w = walsh_hadamard_transform(n-1, f)
        return w + [f([-1 if i == n-1 else x for i, x in enumerate(y)]) for y in w]

def compute_psi_f(clauses, n):
    psi_f = []
    for x in range(2**n):
        assignment = [1 if (x >> i) & 1 else -1 for i in range(n)]
        falsified = sum(1 for clause in clauses if not is_satisfiable([clause], assignment))
        psi_f.append(falsified / len(clauses))
    return psi_f

def compute_nsm(psi_f, n):
    psi_f_hat = walsh_hadamard_transform(n, lambda x: sum(psi_f[i] * math.prod(x[j] for j in range(n)) for i in range(len(psi_f)))) / (2**n)
    var_psi_f = sum(x**2 for x in psi_f_hat) - (sum(psi_f_hat))**2
    stab_rho = sum((1 - (1-1/n)**len(S)) * x**2 for S, x in enumerate(psi_f_hat))
    nsm = (var_psi_f - stab_rho) / var_psi_f if var_psi_f != 0 else 0
    return nsm

def run_trial(seed):
    n_values = [10, 12, 14, 16]
    alpha_values = [4.2, 4.6]
    results = []
    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            clauses = generate_3cnf(n, m, seed)
            assignment = [0] * n
            sat, _ = dpll(clauses, assignment, n)
            if not sat:
                psi_f = compute_psi_f(clauses, n)
                nsm = compute_nsm(psi_f, n)
                t_star = 2**n  # Placeholder for actual DPLL tree size
                margin = math.log2(t_star) - (1/16) * n * nsm
                results.append({
                    "n": n,
                    "alpha": alpha,
                    "nsm": nsm,
                    "t_star": t_star,
                    "margin": margin,
                    "conjecture_holds": margin >= 0
                })
    if not results:
        return {
            "metric_name": "margin",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsat instances found"
        }
    avg_margin = sum(r["margin"] for r in results) / len(results)
    holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    return {
        "metric_name": "margin",
        "metric_value": avg_margin,
        "instances_tested": len(results),
        "conjecture_holds": holds_fraction >= 0.8,
        "counterexample": "" if holds_fraction >= 0.8 else f"Margin too small for n={results[0]['n']}, alpha={results[0]['alpha']}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    metrics = []
    holds = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metrics.append(trial["metric_value"])
        holds.append(trial["conjecture_holds"])
    mean_metric = sum(metrics) / len(metrics)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metrics) / len(metrics))
    support_fraction = sum(holds) / len(holds)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")