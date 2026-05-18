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

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            sign = random.choice([-1, 1])
            clause.append((var, sign))
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, n):
    def dpll(clauses, assignment):
        nonlocal node_count
        node_count += 1
        if node_count > 10**6:
            return False, None
        if not clauses:
            return True, assignment
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var, sign = lit
                if var in assignment and assignment[var] == sign:
                    satisfied = True
                    break
            if not satisfied:
                return False, None
        pure_literals = {}
        for clause in clauses:
            for lit in clause:
                var, sign = lit
                if var not in pure_literals:
                    pure_literals[var] = sign
                elif pure_literals[var] != sign:
                    pure_literals[var] = None
        for var in pure_literals:
            if pure_literals[var] is not None:
                new_assignment = assignment.copy()
                new_assignment[var] = pure_literals[var]
                new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                result, new_assignment = dpll(new_clauses, new_assignment)
                if result:
                    return True, new_assignment
        for clause in clauses:
            for lit in clause:
                var, sign = lit
                if var not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[var] = sign
                    new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                    result, new_assignment = dpll(new_clauses, new_assignment)
                    if result:
                        return True, new_assignment
                    new_assignment = assignment.copy()
                    new_assignment[var] = -sign
                    new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                    result, new_assignment = dpll(new_clauses, new_assignment)
                    if result:
                        return True, new_assignment
                    return False, None
        return False, None
    node_count = 0
    result, _ = dpll(clauses, {})
    return result

def compute_d2(clauses, n, m):
    c_ij_st = defaultdict(int)
    for clause in clauses:
        for (i, s), (j, t) in itertools.combinations(clause, 2):
            if i < j:
                c_ij_st[(i, j, s, t)] += 1
            else:
                c_ij_st[(j, i, t, s)] += 1
    mu_ij_st = m * (3 / n) * (2 / (n - 1)) * (1 / 4)
    max_discrepancy = 0
    for (i, j, s, t) in c_ij_st:
        discrepancy = abs(c_ij_st[(i, j, s, t)] - mu_ij_st)
        if discrepancy > max_discrepancy:
            max_discrepancy = discrepancy
    return max_discrepancy

def compute_t_star(clauses, n):
    def dpll_count(clauses, assignment):
        nonlocal node_count
        node_count += 1
        if node_count > 10**6:
            return 10**6
        if not clauses:
            return 1
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var, sign = lit
                if var in assignment and assignment[var] == sign:
                    satisfied = True
                    break
            if not satisfied:
                return 1
        pure_literals = {}
        for clause in clauses:
            for lit in clause:
                var, sign = lit
                if var not in pure_literals:
                    pure_literals[var] = sign
                elif pure_literals[var] != sign:
                    pure_literals[var] = None
        for var in pure_literals:
            if pure_literals[var] is not None:
                new_assignment = assignment.copy()
                new_assignment[var] = pure_literals[var]
                new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                count = dpll_count(new_clauses, new_assignment)
                if count < 10**6:
                    return count + 1
        for clause in clauses:
            for lit in clause:
                var, sign = lit
                if var not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[var] = sign
                    new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                    count1 = dpll_count(new_clauses, new_assignment)
                    new_assignment = assignment.copy()
                    new_assignment[var] = -sign
                    new_clauses = [c for c in clauses if not any(var == v and sign == s for v, s in c)]
                    count2 = dpll_count(new_clauses, new_assignment)
                    if count1 < 10**6 or count2 < 10**6:
                        return max(count1, count2) + 1
                    return 10**6
        return 1
    node_count = 0
    return dpll_count(clauses, {})

def spearman_rank_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    rank_x = sorted(range(n), key=lambda i: x[i])
    rank_y = sorted(range(n), key=lambda i: y[i])
    d = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    return 1 - (6 * d) / (n * (n ** 2 - 1))

def bootstrap_p_value(x, y, n_resamples=1000):
    n = len(x)
    if n == 0:
        return 1.0
    observed_rho = spearman_rank_correlation(x, y)
    resampled_rhos = []
    for _ in range(n_resamples):
        indices = random.choices(range(n), k=n)
        resampled_x = [x[i] for i in indices]
        resampled_y = [y[i] for i in indices]
        resampled_rho = spearman_rank_correlation(resampled_x, resampled_y)
        resampled_rhos.append(resampled_rho)
    p_value = sum(1 for rho in resampled_rhos if abs(rho) >= abs(observed_rho)) / n_resamples
    return p_value

def run_trial(seed):
    n_sizes = [12, 14, 16, 18, 20]
    alpha = 4.5
    instances = []
    for n in n_sizes:
        m = int(alpha * n)
        for _ in range(6):
            clauses = generate_3cnf(n, m, seed)
            if is_unsatisfiable(clauses, n):
                d2 = compute_d2(clauses, n, m)
                t_star = compute_t_star(clauses, n)
                instances.append((-d2 / math.sqrt(m), math.log2(t_star)))
                break
    if len(instances) < 3:
        return {
            "metric_name": "spearman_rho",
            "metric_value": 0.0,
            "instances_tested": len(instances),
            "conjecture_holds": False,
            "counterexample": "insufficient_unsat_instances"
        }
    x, y = zip(*instances)
    rho = spearman_rank_correlation(x, y)
    p_value = bootstrap_p_value(x, y)
    conjecture_holds = rho >= 0.30 and p_value < 0.05
    return {
        "metric_name": "spearman_rho",
        "metric_value": rho,
        "instances_tested": len(instances),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rho={rho} p_value={p_value}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    metric_values = [trial["metric_value"] for trial in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial["conjecture_holds"] for trial in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for trial in results:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={trial['counterexample']} first_failing_seed={seeds[results.index(trial)]}")
                break