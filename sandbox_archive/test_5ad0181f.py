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

def matrix_mult(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_trace(m):
    n = len(m)
    trace = 0
    for i in range(n):
        trace += m[i][i]
    return trace

def burau_generator(k, n, sign):
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    if sign == 1:
        if k < n - 1:
            m[k][k] = 2
            m[k][k+1] = -1
            m[k+1][k] = -1
    else:
        if k < n - 1:
            m[k][k] = 2
            m[k][k+1] = 1
            m[k+1][k] = 1
    return m

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def is_unsat(clauses, n):
    assignments = []
    for i in range(1, n + 1):
        assignments.append((i, True))
        assignments.append((i, False))
    for assignment in itertools.product(*[assignments]):
        assignment_dict = dict(assignment)
        sat = True
        for clause in clauses:
            clause_sat = False
            for lit in clause:
                var = abs(lit)
                val = assignment_dict[var]
                if (lit > 0 and val) or (lit < 0 and not val):
                    clause_sat = True
                    break
            if not clause_sat:
                sat = False
                break
        if sat:
            return False
    return True

def compute_omega(clauses, n):
    beta = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for clause in clauses:
        sorted_lits = sorted(clause, key=lambda x: abs(x))
        l1, l2, l3 = sorted_lits
        k1 = abs(l1) - 1
        k2 = abs(l2) - 1
        sign1 = 1 if l1 > 0 else -1
        sign2 = 1 if l2 > 0 else -1
        sign3 = 1 if l3 > 0 else -1
        if k1 < n - 1:
            beta = matrix_mult(burau_generator(k1, n, sign1 * sign2), beta)
        if k2 < n - 1:
            beta = matrix_mult(burau_generator(k2, n, sign2 * sign3), beta)
    trace = matrix_trace(beta)
    return abs(n - trace)

def dpll(clauses, assignment, backtracks):
    if not clauses:
        return True, backtracks
    for clause in clauses:
        if len(clause) == 1:
            lit = clause[0]
            var = abs(lit)
            val = lit > 0
            if var in assignment and assignment[var] != val:
                return False, backtracks
            assignment[var] = val
            new_clauses = [c for c in clauses if lit not in c]
            new_clauses = [c for c in new_clauses if -lit not in c]
            sat, backtracks = dpll(new_clauses, assignment.copy(), backtracks)
            if sat:
                return True, backtracks
            else:
                backtracks += 1
                return False, backtracks
    for clause in clauses:
        if len(clause) == 2:
            lit1, lit2 = clause
            var1 = abs(lit1)
            var2 = abs(lit2)
            if var1 not in assignment and var2 not in assignment:
                assignment[var1] = lit1 > 0
                new_clauses = [c for c in clauses if lit1 not in c]
                new_clauses = [c for c in new_clauses if -lit1 not in c]
                sat, backtracks = dpll(new_clauses, assignment.copy(), backtracks)
                if sat:
                    return True, backtracks
                else:
                    backtracks += 1
                    assignment[var1] = lit2 > 0
                    new_clauses = [c for c in clauses if lit2 not in c]
                    new_clauses = [c for c in new_clauses if -lit2 not in c]
                    sat, backtracks = dpll(new_clauses, assignment.copy(), backtracks)
                    if sat:
                        return True, backtracks
                    else:
                        backtracks += 1
                        return False, backtracks
    lit = clauses[0][0]
    var = abs(lit)
    assignment[var] = lit > 0
    new_clauses = [c for c in clauses if lit not in c]
    new_clauses = [c for c in new_clauses if -lit not in c]
    sat, backtracks = dpll(new_clauses, assignment.copy(), backtracks)
    if sat:
        return True, backtracks
    else:
        backtracks += 1
        assignment[var] = not (lit > 0)
        new_clauses = [c for c in clauses if -lit not in c]
        new_clauses = [c for c in new_clauses if lit not in c]
        sat, backtracks = dpll(new_clauses, assignment.copy(), backtracks)
        if sat:
            return True, backtracks
        else:
            backtracks += 1
            return False, backtracks

def compute_t(f, n):
    clauses = [list(clause) for clause in f]
    sat, backtracks = dpll(clauses, {}, 0)
    return backtracks

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = 6 * n
        clauses = generate_3cnf(n, m, seed)
        if is_unsat(clauses, n):
            omega = compute_omega(clauses, n)
            t = compute_t(clauses, n)
            metric_value = 4 * (t ** 2 + 1) - omega
            metric_values.append(metric_value)
            instances_tested += 1
            if metric_value < 0:
                conjecture_holds = False
                counterexample = f"n={n}, seed={seed}, t={t}, omega={omega}"

    if instances_tested == 0:
        return {
            "metric_name": "4*(t^2+1) - omega",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsat instances found"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "4*(t^2+1) - omega",
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
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")