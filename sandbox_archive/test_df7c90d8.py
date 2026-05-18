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

def generate_random_3sat(n, m):
    F = []
    for _ in range(m):
        clause = []
        vars_in_clause = random.sample(range(1, n + 1), 3)
        for v in vars_in_clause:
            if random.random() < 0.5:
                clause.append(-v)
            else:
                clause.append(v)
        F.append(clause)
    return F

def generate_tseitin(n):
    F = []
    edges = list(itertools.combinations(range(1, n + 1), 2))
    for u, v in edges:
        x = len(F) + 1
        F.append([u, v, x])
        F.append([-u, -v, x])
        F.append([u, -v, -x])
        F.append([-u, v, -x])
    return F

def generate_ordering_principle(n):
    F = []
    for i in range(1, n):
        F.append([i, i + 1])
        F.append([-i, -(i + 1)])
    return F

def generate_pebbling(n):
    F = []
    for i in range(1, n):
        F.append([i, i + 1])
        F.append([-i, -(i + 1)])
    return F

def compute_q_hat(F):
    q_hat = defaultdict(float)
    for clause in F:
        vars_in_clause = [abs(lit) for lit in clause]
        signs = [1 if lit < 0 else -1 for lit in clause]
        for T in itertools.combinations(vars_in_clause, 1):
            q_hat[T] += signs[vars_in_clause.index(T[0])] / 8
        for T in itertools.combinations(vars_in_clause, 2):
            q_hat[T] += signs[vars_in_clause.index(T[0])] * signs[vars_in_clause.index(T[1])] / 8
        for T in itertools.combinations(vars_in_clause, 3):
            q_hat[T] += signs[vars_in_clause.index(T[0])] * signs[vars_in_clause.index(T[1])] * signs[vars_in_clause.index(T[2])] / 8
    return q_hat

def compute_norm_2(q_hat):
    norm_2_sq = sum(val ** 2 for val in q_hat.values())
    return math.sqrt(norm_2_sq)

def compute_norm_4(F, n, samples=5000):
    total = 0.0
    for _ in range(samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        q_val = 0.0
        for clause in F:
            product = 1.0
            for lit in clause:
                v = abs(lit)
                s = 1 if lit < 0 else -1
                product *= (1 + s * x[v - 1]) / 2
            q_val += product - 1/8
        total += q_val ** 4
    return (total / samples) ** (1/4)

def dpll_depth(F):
    def backtrack(assignment, clauses):
        if not clauses:
            return 0
        for clause in clauses:
            if all(lit in assignment for lit in clause):
                continue
            if any(-lit in assignment for lit in clause):
                continue
            break
        else:
            return 0

        unassigned_vars = set()
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in assignment:
                    unassigned_vars.add(abs(lit))
        if not unassigned_vars:
            return float('inf')

        var = unassigned_vars.pop()
        new_clauses = [clause for clause in clauses if var not in [abs(lit) for lit in clause]]

        depth1 = backtrack(assignment.copy(), new_clauses)
        if depth1 != float('inf'):
            depth1 += 1

        depth2 = backtrack(assignment.copy(), new_clauses)
        if depth2 != float('inf'):
            depth2 += 1

        return min(depth1, depth2)

    return backtrack({}, F)

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16]
    ensemble_generators = [generate_random_3sat, generate_tseitin, generate_ordering_principle, generate_pebbling]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for generator in ensemble_generators:
            if generator == generate_random_3sat:
                m = int(5.0 * n)
                F = generator(n, m)
            else:
                F = generator(n)

            q_hat = compute_q_hat(F)
            norm_2 = compute_norm_2(q_hat)
            norm_4 = compute_norm_4(F, n)
            r_F = norm_4 / norm_2
            G_F = (3 ** (3/2) - r_F) / 3 ** (3/2)
            d_star_F = dpll_depth(F)

            if d_star_F == float('inf'):
                continue

            instances_tested += 1
            metric_value = math.log2(d_star_F + 1) / (n * G_F) if G_F > 0 else float('inf')
            metric_values.append(metric_value)

            if metric_value < 0.05:
                conjecture_holds = False
                counterexample = f"n={n}, ensemble={generator.__name__}, d*(F)={d_star_F}, G(F)={G_F}"

    if not metric_values:
        return {
            "metric_name": "log2(d*(F)+1)/(n*G(F))",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    return {
        "metric_name": "log2(d*(F)+1)/(n*G(F))",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trial_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        trial_results.append(result)

    metric_values = [r["metric_value"] for r in trial_results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in trial_results if r["conjecture_holds"]) / len(trial_results)

    if all(r["conjecture_holds"] for r in trial_results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in trial_results):
        first_failing_seed = seeds[trial_results.index(next(r for r in trial_results if not r["conjecture_holds"]))]
        counterexample = next(r["counterexample"] for r in trial_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")