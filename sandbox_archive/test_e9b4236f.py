# auto-injected by SEC sandbox
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict
from itertools import combinations

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
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
        nonlocal nodes
        nodes += 1
        if nodes > 10**6:
            return None

        if not clauses:
            return True

        for clause in clauses:
            satisfied = False
            for lit in clause:
                var, sign = lit
                if var in assignment and assignment[var] == sign:
                    satisfied = True
                    break
            if not satisfied:
                return False

        for var in range(1, n + 1):
            if var not in assignment:
                for sign in [-1, 1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = sign
                    if dpll(clauses, new_assignment):
                        return True
                return False
        return False

    nodes = 0
    return dpll(clauses, {}) is False

def compute_d2(clauses, n, m):
    c_ij_st = defaultdict(int)
    for clause in clauses:
        for (var1, sign1), (var2, sign2) in combinations(clause, 2):
            if var1 < var2:
                c_ij_st[(var1, var2, sign1, sign2)] += 1
            else:
                c_ij_st[(var2, var1, sign2, sign1)] += 1

    mu_ij_st = m * (3 / n) * (2 / (n - 1)) * (1 / 4)
    max_diff = 0
    for (i, j, s, t) in c_ij_st:
        diff = abs(c_ij_st[(i, j, s, t)] - mu_ij_st)
        if diff > max_diff:
            max_diff = diff
    return max_diff

def spearman_rank_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    rank_x = sorted(range(n), key=lambda i: x[i])
    rank_y = sorted(range(n), key=lambda i: y[i])
    d_squared = sum((rank_x[i] - rank_y[i])**2 for i in range(n))
    return 1 - (6 * d_squared) / (n * (n**2 - 1))

def run_trial(seed):
    n_values = [12, 14, 16, 18, 20]
    alpha = 4.5
    instances = []
    for n in n_values:
        m = int(alpha * n)
        attempts = 0
        while attempts < 100:
            clauses = generate_3cnf(n, m, seed + attempts)
            if is_unsatisfiable(clauses, n):
                d2 = compute_d2(clauses, n, m)
                instances.append((n, m, d2))
                break
            attempts += 1

    if len(instances) < len(n_values):
        return {
            "metric_name": "spearman_correlation",
            "metric_value": 0.0,
            "instances_tested": len(instances),
            "conjecture_holds": False,
            "counterexample": "failed_to_generate_unsat_instances"
        }

    x = [-d2 / math.sqrt(m) for (n, m, d2) in instances]
    y = [math.log2(m) for (n, m, d2) in instances]
    correlation = spearman_rank_correlation(x, y)

    return {
        "metric_name": "spearman_correlation",
        "metric_value": correlation,
        "instances_tested": len(instances),
        "conjecture_holds": correlation >= 0.30,
        "counterexample": "" if correlation >= 0.30 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **trial})}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((seeds[i] for i, trial in enumerate(trials) if not trial["conjecture_holds"]), None)
        if first_failing_seed is not None:
            print(f"RESULT: FALSIFIED counterexample=\"{trials[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=unknown")