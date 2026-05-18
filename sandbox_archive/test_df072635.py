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
            if random.choice([True, False]):
                clause.append((v, 1))
            else:
                clause.append((v, -1))
        clauses.append(clause)
    return clauses

def generate_tseitin_3cnf(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        n += 1
    edges = list(itertools.combinations(range(n), 2))
    random.shuffle(edges)
    clauses = []
    for u, v in edges[:n//2]:
        clauses.append([(u, 1), (v, 1), (n + u, -1)])
        clauses.append([(u, -1), (v, -1), (n + u, 1)])
    return clauses

def generate_ordering_principle_3cnf(n, seed):
    random.seed(seed)
    clauses = []
    for i in range(n - 1):
        clauses.append([(i, 1), (i + 1, -1)])
    return clauses

def generate_pebbling_3cnf(n, seed):
    random.seed(seed)
    clauses = []
    for i in range(n - 1):
        clauses.append([(i, 1), (i + 1, -1)])
    return clauses

def is_satisfiable(clauses, n):
    def backtrack(assignment, clause_index):
        if clause_index == len(clauses):
            return True
        clause = clauses[clause_index]
        for var, sign in clause:
            if var not in assignment:
                for val in [1, -1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    if backtrack(new_assignment, clause_index + 1):
                        return True
                return False
        if any(assignment.get(var, 0) * sign == -1 for var, sign in clause):
            return backtrack(assignment, clause_index + 1)
        return False
    return backtrack({}, 0)

def compute_qf_hat(clauses, T):
    qf_hat = 0.0
    for clause in clauses:
        vars_in_clause = [var for var, _ in clause]
        if all(v in T for v in vars_in_clause):
            product = 1.0
            for var, sign in clause:
                if var in T:
                    product *= sign
            qf_hat += product
    return (1/8) * qf_hat

def compute_qf_norm_2(clauses, n):
    norm_2_squared = 0.0
    for T in itertools.chain.from_iterable(itertools.combinations(range(n), r) for r in [1, 2, 3]):
        qf_hat = compute_qf_hat(clauses, T)
        norm_2_squared += qf_hat ** 2
    return math.sqrt(norm_2_squared)

def compute_qf_norm_4(clauses, n, num_samples=5000):
    total = 0.0
    for _ in range(num_samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        qf = 0.0
        for clause in clauses:
            term = 1.0
            for var, sign in clause:
                term *= (1 + sign * x[var]) / 2
            qf += term - 1/8
        total += qf ** 4
    return (total / num_samples) ** (1/4)

def compute_d_star(clauses, n):
    def backtrack(assignment, clause_index, depth):
        if clause_index == len(clauses):
            return depth
        clause = clauses[clause_index]
        for var, sign in clause:
            if var not in assignment:
                for val in [1, -1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    result = backtrack(new_assignment, clause_index + 1, depth + 1)
                    if result is not None:
                        return result
                return None
        if any(assignment.get(var, 0) * sign == -1 for var, sign in clause):
            return backtrack(assignment, clause_index + 1, depth)
        return None
    return backtrack({}, 0, 0)

def run_trial(seed):
    n_values = [10, 12, 14, 16]
    ensemble_generators = [
        lambda n, seed: generate_random_3cnf(n, 5 * n, seed),
        lambda n, seed: generate_tseitin_3cnf(n, seed),
        lambda n, seed: generate_ordering_principle_3cnf(n, seed),
        lambda n, seed: generate_pebbling_3cnf(n, seed)
    ]
    results = []
    for n in n_values:
        for generator in ensemble_generators:
            clauses = generator(n, seed)
            if not is_satisfiable(clauses, n):
                norm_2 = compute_qf_norm_2(clauses, n)
                norm_4 = compute_qf_norm_4(clauses, n)
                r_f = norm_4 / norm_2
                g_f = (3 ** (3/2) - r_f) / (3 ** (3/2))
                d_star = compute_d_star(clauses, n)
                metric_value = math.log2(d_star + 1) / (0.05 * n * g_f) if g_f > 0 else float('inf')
                conjecture_holds = metric_value >= 1.0
                counterexample = "" if conjecture_holds else f"d*(F)={d_star}, G(F)={g_f}, n={n}"
                results.append({
                    "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
                    "metric_value": metric_value,
                    "instances_tested": 1,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                })
    if not results:
        return {
            "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances generated"
        }
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        return {
            "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
            "metric_value": mean_metric,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": "",
            "mean": mean_metric,
            "std": std_metric,
            "support_fraction": support_fraction
        }
    else:
        first_failing_index = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        return {
            "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
            "metric_value": mean_metric,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": results[first_failing_index]["counterexample"],
            "first_failing_seed": seed,
            "mean": mean_metric,
            "std": std_metric,
            "support_fraction": support_fraction
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    metric_values = [r["metric_value"] for r in all_results if "metric_value" in r]
    if metric_values:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(r["conjecture_holds"] for r in all_results) / len(all_results)
        if all(r["conjecture_holds"] for r in all_results):
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_index = next(i for i, r in enumerate(all_results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{all_results[first_failing_index]['counterexample']}\" first_failing_seed={seeds[first_failing_index]}")
    else:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")