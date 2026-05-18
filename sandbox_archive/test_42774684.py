# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
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

def generate_tseitin(n, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for i in range(n):
        a, b, c = random.sample(variables, 3)
        clauses.append([(a, 1), (b, 1), (i, -1)])
        clauses.append([(a, 1), (c, 1), (i, -1)])
        clauses.append([(b, 1), (c, 1), (i, -1)])
        clauses.append([(a, -1), (b, -1), (c, -1), (i, 1)])
    return clauses

def generate_ordering_principle(n):
    variables = list(range(n))
    clauses = []
    for i in range(n):
        for j in range(i+1, n):
            clauses.append([(i, 1), (j, -1)])
    return clauses

def generate_pebbling(n, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for i in range(n):
        if i > 0:
            clauses.append([(i, 1), (i-1, -1)])
    return clauses

def compute_q_hat(F):
    q_hat = defaultdict(float)
    for clause in F:
        vars_in_clause = [v for v, _ in clause]
        for t_size in [1, 2, 3]:
            for T in itertools.combinations(vars_in_clause, t_size):
                product = 1.0
                for v in T:
                    for (var, sign) in clause:
                        if var == v:
                            product *= sign
                            break
                q_hat[T] += product
    for T in q_hat:
        q_hat[T] *= 0.125
    return q_hat

def compute_norm_2_squared(q_hat):
    norm_2_squared = 0.0
    for T in q_hat:
        norm_2_squared += q_hat[T] ** 2
    return norm_2_squared

def compute_norm_4_fourth(q_hat, n, seed):
    random.seed(seed)
    total = 0.0
    samples = 5000
    for _ in range(samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        q_value = 0.0
        for clause in q_hat:
            product = 1.0
            for v in clause:
                product *= (1 + q_hat[clause] * x[v]) / 2 - 1/8
            q_value += product
        total += q_value ** 4
    return total / samples

def dpll_depth(F, assignment=None, depth=0):
    if assignment is None:
        assignment = {}
    unassigned = [v for v in range(len(F)) if v not in assignment]
    if not unassigned:
        return depth
    var = unassigned[0]
    for value in [-1, 1]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if not any(all(assignment.get(abs(lit), 0) == lit for lit in clause) for clause in F):
            continue
        result = dpll_depth(F, new_assignment, depth + 1)
        if result is not None:
            return result
    return None

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    results = []
    for n in n_values:
        m = 5 * n
        F_random = generate_random_3cnf(n, m, seed)
        F_tseitin = generate_tseitin(n, seed)
        F_ordering = generate_ordering_principle(n)
        F_pebbling = generate_pebbling(n, seed)
        for F in [F_random, F_tseitin, F_ordering, F_pebbling]:
            q_hat = compute_q_hat(F)
            norm_2_squared = compute_norm_2_squared(q_hat)
            norm_4_fourth = compute_norm_4_fourth(q_hat, n, seed)
            if norm_2_squared == 0:
                continue
            r_F = (norm_4_fourth ** 0.25) / (norm_2_squared ** 0.5)
            G_F = (3 ** 1.5 - r_F) / (3 ** 1.5)
            d_star_F = dpll_depth(F)
            if d_star_F is None:
                d_star_F = 0
            metric_value = math.log2(d_star_F + 1) / (0.05 * n * G_F) if G_F != 0 else float('inf')
            conjecture_holds = metric_value >= 1
            counterexample = f"n={n}, d*(F)={d_star_F}, G(F)={G_F}, metric_value={metric_value}" if not conjecture_holds else ""
            results.append({
                "seed": seed,
                "metric_name": "log2(d*(F)+1) / (0.05 * n * G(F))",
                "metric_value": metric_value,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    return results

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_results = run_trial(seed)
        for result in trial_results:
            print(f"TRIAL: {result}")
            results.append(result)
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != float('inf')]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=all_inf")
    else:
        mean = sum(metric_values) / len(metric_values)
        std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")