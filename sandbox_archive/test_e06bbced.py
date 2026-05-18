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

def generate_random_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for v in clause_vars:
            sign = random.choice([-1, 1])
            clause.append((v, sign))
        clauses.append(clause)
    return clauses

def generate_tseitin_3cnf(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        n += 1
    variables = list(range(n))
    clauses = []
    for i in range(0, n, 2):
        v1, v2 = variables[i], variables[i+1]
        s1 = random.choice([-1, 1])
        s2 = random.choice([-1, 1])
        clauses.append([(v1, s1), (v2, s2)])
        clauses.append([(v1, -s1), (v2, -s2)])
    return clauses

def generate_ordering_principle_3cnf(n, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for i in range(n-1):
        v1, v2 = variables[i], variables[i+1]
        s1 = random.choice([-1, 1])
        s2 = random.choice([-1, 1])
        clauses.append([(v1, s1), (v2, s2)])
        clauses.append([(v1, -s1), (v2, -s2)])
    return clauses

def generate_pebbling_3cnf(n, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for i in range(1, n):
        v1, v2 = variables[i-1], variables[i]
        s1 = random.choice([-1, 1])
        s2 = random.choice([-1, 1])
        clauses.append([(v1, s1), (v2, s2)])
        clauses.append([(v1, -s1), (v2, -s2)])
    return clauses

def is_unsatisfiable(clauses, n):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        for clause in clauses:
            if all((v in assignment and assignment[v] == -s) or (v not in assignment) for v, s in clause):
                continue
            if any(v not in assignment for v, s in clause):
                for v, s in clause:
                    if v not in assignment:
                        new_assignment = assignment.copy()
                        new_assignment[v] = s
                        if dpll([c for c in clauses if c != clause], new_assignment):
                            return True
                        new_assignment[v] = -s
                        if dpll([c for c in clauses if c != clause], new_assignment):
                            return True
                return False
        return False
    return not dpll(clauses, {})

def compute_qf_hat(clauses, n):
    qf_hat = defaultdict(float)
    for clause in clauses:
        vars_in_clause = [v for v, s in clause]
        for T in itertools.combinations(vars_in_clause, 1):
            T = set(T)
            product = 1.0
            for v, s in clause:
                if v in T:
                    product *= s
            qf_hat[tuple(T)] += product
        for T in itertools.combinations(vars_in_clause, 2):
            T = set(T)
            product = 1.0
            for v, s in clause:
                if v in T:
                    product *= s
            qf_hat[tuple(T)] += product
        for T in itertools.combinations(vars_in_clause, 3):
            T = set(T)
            product = 1.0
            for v, s in clause:
                if v in T:
                    product *= s
            qf_hat[tuple(T)] += product
    for T in qf_hat:
        qf_hat[T] *= 0.125
    return qf_hat

def compute_norm_2_squared(qf_hat):
    norm_2_squared = 0.0
    for T in qf_hat:
        norm_2_squared += qf_hat[T] ** 2
    return norm_2_squared

def compute_norm_4_fourth(qf_hat, n, seed):
    random.seed(seed)
    norm_4_fourth = 0.0
    for _ in range(5000):
        x = [random.choice([-1, 1]) for _ in range(n)]
        qf_x = 0.0
        for clause in qf_hat:
            product = 1.0
            for v in clause:
                product *= (1 + qf_hat[clause] * x[v]) / 2
            qf_x += product - 0.125
        norm_4_fourth += qf_x ** 4
    norm_4_fourth /= 5000
    return norm_4_fourth

def compute_d_star(clauses, n):
    def dpll_depth(clauses, assignment, depth):
        if not clauses:
            return depth
        min_depth = float('inf')
        for clause in clauses:
            if all((v in assignment and assignment[v] == -s) or (v not in assignment) for v, s in clause):
                continue
            if any(v not in assignment for v, s in clause):
                for v, s in clause:
                    if v not in assignment:
                        new_assignment = assignment.copy()
                        new_assignment[v] = s
                        current_depth = dpll_depth([c for c in clauses if c != clause], new_assignment, depth + 1)
                        if current_depth < min_depth:
                            min_depth = current_depth
                        new_assignment[v] = -s
                        current_depth = dpll_depth([c for c in clauses if c != clause], new_assignment, depth + 1)
                        if current_depth < min_depth:
                            min_depth = current_depth
                return min_depth
        return depth
    return dpll_depth(clauses, {}, 0)

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = int(5.0 * n)
        for _ in range(4):
            clauses = generate_random_3cnf(n, m, seed)
            if is_unsatisfiable(clauses, n):
                qf_hat = compute_qf_hat(clauses, n)
                norm_2_squared = compute_norm_2_squared(qf_hat)
                norm_4_fourth = compute_norm_4_fourth(qf_hat, n, seed)
                norm_2 = math.sqrt(norm_2_squared)
                norm_4 = norm_4_fourth ** 0.25
                r_f = norm_4 / norm_2 if norm_2 > 0 else 0.0
                g_f = (3 ** 1.5 - r_f) / 3 ** 1.5 if r_f <= 3 ** 1.5 else 0.0
                d_star = compute_d_star(clauses, n)
                if d_star is None:
                    d_star = 0
                metric_value = math.log2(d_star + 1) / (0.05 * n * g_f) if g_f > 0 else float('inf')
                metric_values.append(metric_value)
                instances_tested += 1
                if metric_value < 1.0:
                    conjecture_holds = False
                    counterexample = f"n={n}, d*(F)={d_star}, G(F)={g_f}, metric_value={metric_value}"

    if instances_tested == 0:
        return {
            "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
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

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    else:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")