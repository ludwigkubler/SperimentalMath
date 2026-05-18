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
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def generate_tseitin_cnf(n, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    edges = list(itertools.combinations(variables, 2))
    random.shuffle(edges)
    clauses = []
    for u, v in edges[:n]:
        w = random.choice(variables)
        clauses.append([u, v, -w])
        clauses.append([u, -v, w])
        clauses.append([-u, v, w])
        clauses.append([-u, -v, -w])
    return clauses

def generate_trivial_unsat(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            clause[i] = -clause[i]
        clauses.append(clause)
    return clauses

def is_satisfiable(clauses, assignment):
    for clause in clauses:
        if all((lit > 0 and assignment.get(abs(lit), False)) or (lit < 0 and not assignment.get(abs(lit), False)) for lit in clause):
            return True
    return False

def dpll(clauses, assignment, variables, max_nodes):
    if max_nodes <= 0:
        return None
    if not clauses:
        return assignment
    if any(not clause for clause in clauses):
        return None
    var = max(variables, key=lambda v: sum(1 for clause in clauses if v in clause or -v in clause))
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        new_clauses = []
        for clause in clauses:
            new_clause = [lit for lit in clause if not ((lit > 0 and new_assignment.get(lit, False)) or (lit < 0 and not new_assignment.get(abs(lit), False)))]
            if not new_clause:
                return None
            new_clauses.append(new_clause)
        result = dpll(new_clauses, new_assignment, [v for v in variables if v != var], max_nodes - 1)
        if result is not None:
            return result
    return None

def compute_t_star(clauses, variables):
    max_nodes = 2 * 10**6
    result = dpll(clauses, {}, variables, max_nodes)
    if result is None:
        return max_nodes
    return max_nodes - sum(1 for _ in range(max_nodes) if dpll(clauses, {}, variables, _) is not None)

def compute_l1(clauses, n):
    l1 = 0.0
    for clause in clauses:
        for S in itertools.product([-1, 1], repeat=n):
            if len([s for s in S if s == 1]) > 3:
                continue
            p = 1.0
            for lit in clause:
                if lit > 0:
                    p *= (1 + S[lit - 1]) / 2
                else:
                    p *= (1 - S[abs(lit) - 1]) / 2
            l1 += abs(p)
    return l1

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    m_values = [5, 10, 15, 20, 25]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for m in m_values:
            if n * m > 36:
                continue
            for family in ['tseitin', 'random', 'trivial']:
                if family == 'tseitin':
                    clauses = generate_tseitin_cnf(n, seed)
                elif family == 'random':
                    clauses = generate_random_3cnf(n, m, seed)
                else:
                    clauses = generate_trivial_unsat(n, m, seed)
                if not is_satisfiable(clauses, {}):
                    l1 = compute_l1(clauses, n)
                    t_star = compute_t_star(clauses, list(range(1, n + 1)))
                    metric_value = l1 / math.sqrt(m + 1)
                    bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
                    if metric_value > bound:
                        conjecture_holds = False
                        counterexample = f"n={n}, m={m}, family={family}, l1={l1}, t_star={t_star}, metric_value={metric_value}, bound={bound}"
                        break
                    metric_values.append(metric_value)
                    instances_tested += 1
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "L1/Fourier_mass_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    return {
        "metric_name": "L1/Fourier_mass_ratio",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")