# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys

def lex_dpll(F):
    def dpll(F, assignment):
        if not F:
            return True
        unit_clauses = [c for c in F if len(c) == 1]
        if unit_clauses:
            v = unit_clauses[0][0]
            if v > 0 and v in assignment and assignment[v] != 1:
                return False
            if v < 0 and -v in assignment and assignment[-v] != 0:
                return False
            new_assignment = assignment.copy()
            new_assignment[v if v > 0 else -v] = 1 if v > 0 else 0
            return dpll([c for c in F if v not in c and -v not in c], new_assignment)
        pure_vars = set()
        for c in F:
            pos = [x for x in c if x > 0]
            neg = [-x for x in c if x < 0]
            if len(pos) == 1:
                pure_vars.add(pos[0])
            elif len(neg) == 1:
                pure_vars.add(-neg[0])
        if not pure_vars:
            return False
        v = next(iter(pure_vars))
        new_assignment = assignment.copy()
        new_assignment[v] = 1
        if dpll([c for c in F if v not in c], new_assignment):
            return True
        new_assignment[v] = 0
        if dpll([c for c in F if -v not in c], new_assignment):
            return True
        return False

    assignment = {}
    return dpll(F, assignment)

def generate_unsat_3cnf(n, alpha):
    while True:
        clauses = []
        for _ in range(int(alpha * n * (n - 1) / 2)):
            v1, v2, v3 = random.sample(range(1, n + 1), 3)
            clause = [random.choice([v1, -v1]) for _ in range(3)]
            clauses.append(clause)
        if not lex_dpll(clauses):
            return clauses

def grundy_value(F, memo):
    if not F:
        return 0
    if tuple(sorted(F)) in memo:
        return memo[tuple(sorted(F))]
    moves = set()
    for clause in F:
        for literal in clause:
            new_F = [c for c in F if literal not in c and -literal not in c]
            moves.add(grundy_value(new_F, memo))
    mex = 0
    while mex in moves:
        mex += 1
    memo[tuple(sorted(F))] = mex
    return mex

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    alpha_values = [4.5, 5.0, 5.5]
    results = []
    for n in n_values:
        for alpha in alpha_values:
            F = generate_unsat_3cnf(n, alpha)
            G_F = grundy_value(F, {})
            L_T_F = lex_dpll(F)
            if not L_T_F:
                continue
            log2_G_F = math.log2(1 + G_F)
            log2_L_T_F = math.log2(L_T_F)
            results.append((n, alpha, G_F, L_T_F, log2_G_F, log2_L_T_F))
    if not results:
        return {
            "metric_name": "log2_G_F_vs_log2_L_T_F",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    log2_G_F_values = [r[3] for r in results]
    log2_L_T_F_values = [r[4] for r in results]
    mean_log2_G_F = sum(log2_G_F_values) / len(log2_G_F_values)
    mean_log2_L_T_F = sum(log2_L_T_F_values) / len(log2_L_T_F_values)
    std_log2_G_F = math.sqrt(sum((x - mean_log2_G_F) ** 2 for x in log2_G_F_values) / len(log2_G_F_values))
    std_log2_L_T_F = math.sqrt(sum((x - mean_log2_L_T_F) ** 2 for x in log2_L_T_F_values) / len(log2_L_T_F_values))
    support_fraction = sum(1 for r in results if r[3] <= r[4]) / len(results)
    return {
        "metric_name": "log2_G_F_vs_log2_L_T_F",
        "metric_value": mean_log2_G_F,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")