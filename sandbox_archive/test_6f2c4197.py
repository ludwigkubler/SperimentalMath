# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import math
import random
import json
import collections

def make_planted_3cnf(n, m, rng):
    assignment = [rng.randint(0, 1) for _ in range(n+1)]
    clauses = []
    attempts = 0
    while len(clauses) < m and attempts < m * 100:
        attempts += 1
        vars_ = rng.sample(range(1, n+1), 3)
        lits = []
        for v in vars_:
            if rng.random() < 0.5:
                lits.append(v)
            else:
                lits.append(-v)
        satisfied = any((l > 0 and assignment[l] == 1) or (l < 0 and assignment[-l] == 0) for l in lits)
        if not satisfied:
            flip = rng.choice(lits)
            if flip > 0:
                assignment[flip] = 1
            else:
                assignment[-flip] = 0
        clauses.append(tuple(lits))
    return clauses

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            unset = []
            satisfied = False
            for l in cl:
                v = abs(l)
                if v in assignment:
                    if (l > 0 and assignment[v] == 1) or (l < 0 and assignment[v] == 0):
                        satisfied = True
                        break
                else:
                    unset.append(l)
            if satisfied:
                continue
            if len(unset) == 0:
                return None
            if len(unset) == 1:
                l = unset[0]
                v = abs(l)
                val = 1 if l > 0 else 0
                if v in assignment and assignment[v] != val:
                    return None
                assignment[v] = val
                changed = True
    return assignment

def jw_score(clauses, assignment, var):
    score = [0.0, 0.0]
    for cl in clauses:
        unset = []
        satisfied = False
        for l in cl:
            v = abs(l)
            if v in assignment:
                if (l > 0 and assignment[v] == 1) or (l < 0 and assignment[v] == 0):
                    satisfied = True
                    break
            else:
                unset.append(l)
        if satisfied or len(unset) == 0:
            continue
        for l in unset:
            if abs(l) == var:
                idx = 0 if l > 0 else 1
                score[idx] += 2.0 ** (-len(unset))
    return score

def dpll(clauses, assignment, depth, max_depth):
    assignment = dict(assignment)
    result = unit_propagate(clauses, assignment)
    if result is None:
        return None, depth
    assignment = result
    active_vars = set()
    all_satisfied = True
    for cl in clauses:
        satisfied = False
        for l in cl:
            v = abs(l)
            if v in assignment:
                if (l > 0 and assignment[v] == 1) or (l < 0 and assignment[v] == 0):
                    satisfied = True
                    break
        if not satisfied:
            all_satisfied = False
            for l in cl:
                v = abs(l)
                if v not in assignment:
                    active_vars.add(v)
    if all_satisfied:
        return assignment, depth
    if not active_vars:
        return None, depth
    if depth >= max_depth:
        return None, depth
    best_var = None
    best_score = -1
    for var in active_vars:
        sc = jw_score(clauses, assignment, var)
        s = sc[0] + sc[1]
        if s > best_score:
            best_score = s
            best_var = var
    for val in [1, 0]:
        new_assign = dict(assignment)
        new_assign[best_var] = val
        res, d = dpll(clauses, new_assign, depth + 1, max_depth)
        if res is not None:
            return res, d
    return None, depth

def dpll_depth(clauses, n):
    sys.setrecursionlimit(10000)
    max_depth = n * 4
    _, d = dpll(clauses, {}, 0, max_depth)
    return d

def is_clause_satisfied(clause, assignment):
    for l in clause:
        v = abs(l)
        if v in assignment:
            if (l > 0 and assignment[v] == 1) or (l < 0 and assignment[v] == 0):
                return True
    return False

def resolution_width_lower_bound(clauses, n, max_w):
    initial = set()
    for cl in clauses:
        initial.add(frozenset(cl))
    derived = set(initial)
    for w in range(0, max_w + 1):
        prev_size = -1
        while prev_size != len(derived):
            prev_size = len(derived)
            new_clauses = set()
            derived_list = list(derived)
            for i in range(len(derived_list)):
                if len(derived_list[i]) > w:
                    continue
                for j in range(i, len(derived_list)):
                    if len(derived_list[j]) > w:
                        continue
                    ci = derived_list[i]
                    cj = derived_list[j]
                    resolvents = []
                    for l in ci:
                        if -l in cj:
                            resolvent = (ci - {l}) | (cj - {-l})
                            resolvents.append(resolvent)
                    for r in resolvents:
                        if len(r) <= w:
                            new_clauses.add(frozenset(r))
            for nc in new_clauses:
                derived.add(nc)
        if frozenset() in derived:
            return w
    return max_w + 1

def compute_width_star(clauses, n):
    max_w = min(n, 8)
    w = resolution_width_lower_bound(clauses, n, max_w)
    return w

def quantile(data, p):
    s = sorted(data)
    idx = p * (len(s) - 1)
    lo = int(idx)
    hi = lo + 1
    if hi >= len(s):
        return float(s[-1])
    frac = idx - lo
    return s[lo] * (1 - frac) + s[hi] * frac

def run_trial(seed: int) -> dict:
    rng = random.Random(seed)
    N_samples = 200
    ns = [10, 12, 14, 16, 18, 20]
    density = 4.2
    c1 = 0.25
    c2 = 2.0
    log100 = math.log(100)

    all_hold = True
    counterexample = ""
    instances_tested = 0
    metric_values = []

    for n in ns:
        m = int(density * n)
        depths = []
        formulas = []
        for _ in range(N_samples):
            clauses = make_planted_3cnf(n, m, rng)
            d = dpll_depth(clauses, n)
            depths.append(d)
            formulas.append(clauses)
            instances_tested += 1

        q50 = quantile(depths, 0.5)
        q90 = quantile(depths, 0.9)
        q99 = quantile(depths, 0.99)
        beta_n = q90 - q50

        max_d = max(depths)
        f_max = formulas[depths.index(max_d)]

        w_star = compute_width_star(f_max, n)

        lo = c1 * q99
        hi = c2 * q50 * log100

        ratio = w_star / (q99 + 1e-9)
        metric_values.append(ratio)

        holds_n = (lo <= w_star <= hi)
        if not holds_n:
            all_hold = False
            counterexample = (
                f"n={n}: W*={w_star}, Q0.5={q50:.2f}, Q0.99={q99:.2f}, "
                f"beta={beta_n:.2f}, lo={lo:.2f}, hi={hi:.2f}; "
                f"condition {'lo>W*' if w_star < lo else 'W*>hi'} violated"
            )

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0

    return {
        "metric_name": "mean_W*_over_Q0.99_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all_hold,
        "counterexample": counterexample,
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]

    results = []
    first_failing_seed = None
    first_counterexample = ""

    for seed in seeds:
        trial = run_trial(seed)
        row = {"seed": seed, **trial}
        print("TRIAL:", json.dumps(row))
        results.append(trial)
        if not trial["conjecture_holds"] and first_failing_seed is None:
            first_failing_seed = seed
            first_counterexample = trial["counterexample"]

    values = [r["metric_value"] for r in results]
    n_res = len(values)
    mean_v = sum(values) / n_res
    std_v = math.sqrt(sum((x - mean_v) ** 2 for x in values) / n_res) if n_res > 1 else 0.0
    support_frac = sum(1 for r in results if r["conjecture_holds"]) / n_res

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{first_counterexample}" first_failing_seed={first_failing_seed}')
    elif support_frac >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_v:.4f} std={std_v:.4f} support_fraction={support_frac:.2f}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_frac:.2f} mean={mean_v:.4f} std={std_v:.4f}")