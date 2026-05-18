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

def generate_random_3cnf(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def generate_tseitin_graph(n):
    if n % 2 != 0:
        n += 1
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def generate_tseitin_cnf(edges, n):
    clauses = []
    for i, (u, v) in enumerate(edges):
        clauses.append([u + 1, v + 1, i + n + 1])
        clauses.append([-u - 1, -v - 1, i + n + 1])
        clauses.append([u + 1, -v - 1, -i - n - 1])
        clauses.append([-u - 1, v + 1, -i - n - 1])
    return clauses

def is_satisfiable(clauses, n):
    def backtrack(assignment, clause_index):
        if clause_index == len(clauses):
            return True
        clause = clauses[clause_index]
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                assignment[var] = literal > 0
                if backtrack(assignment, clause_index + 1):
                    return True
                del assignment[var]
        return False
    return backtrack({}, 0)

def compute_l1_fourier_mass(clauses, n):
    def walsh_coefficient(clause, S):
        sign = 1
        for literal in clause:
            var = abs(literal)
            if var in S:
                sign *= -1 if literal < 0 else 1
        return sign

    fourier_mass = 0.0
    for clause in clauses:
        for S in itertools.product([False, True], repeat=n):
            S = {i + 1 for i, val in enumerate(S) if val}
            if 1 <= len(S) <= 3:
                fourier_mass += abs(walsh_coefficient(clause, S))
    return fourier_mass / (2 ** n)

def compute_dpll_tree_size(clauses, n):
    def dpll(assignment, clause_index):
        if clause_index == len(clauses):
            return 1
        clause = clauses[clause_index]
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                assignment[var] = literal > 0
                size = dpll(assignment, clause_index + 1)
                del assignment[var]
                return size + 1
        return 1

    return dpll({}, 0)

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Generate Tseitin CNF
        edges = generate_tseitin_graph(n)
        clauses = generate_tseitin_cnf(edges, n)
        if not is_satisfiable(clauses, n + len(edges)):
            l1 = compute_l1_fourier_mass(clauses, n + len(edges))
            m = len(clauses)
            t_star = compute_dpll_tree_size(clauses, n + len(edges))
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Tseitin CNF with n={n}, m={m}, L1={l1}, t*={t_star}"
                break
            metric_values.append(ratio)
            instances_tested += 1

        # Generate random 3-CNF
        m = int(5.0 * n)
        clauses = generate_random_3cnf(n, m)
        if not is_satisfiable(clauses, n):
            l1 = compute_l1_fourier_mass(clauses, n)
            t_star = compute_dpll_tree_size(clauses, n)
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Random 3-CNF with n={n}, m={m}, L1={l1}, t*={t_star}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if conjecture_holds and len(metric_values) > 0:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        return {
            "metric_name": "L1/Fourier mass ratio",
            "metric_value": mean,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample,
            "std": std
        }
    else:
        return {
            "metric_name": "L1/Fourier mass ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample,
            "std": 0.0
        }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if metric_values:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            falsified = [r for r in results if not r["conjecture_holds"]]
            if falsified:
                first_failing_seed = seeds[results.index(falsified[0])]
                print(f"RESULT: FALSIFIED counterexample=\"{falsified[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
            else:
                print("RESULT: INCONCLUSIVE reason=insufficient_support")
    else:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")