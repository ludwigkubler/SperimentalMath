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

def dpll(clauses, assignment):
    if not clauses:
        return True
    for literal in range(len(assignment)):
        if assignment[literal] is None:
            for value in [True, False]:
                new_assignment = assignment[:]
                new_assignment[literal] = value
                if dpll([c for c in clauses if not (len(c) == 1 and c[0] == -literal)], new_assignment):
                    return True
            return False
    return False

def is_unsat(clauses):
    assignment = [None] * len(clauses)
    return not dpll(clauses, assignment)

def count_unsat(clauses):
    n = len(clauses)
    count = 0
    for i in range(1 << n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if is_unsat([c for c in clauses]):
            count += 1
    return count

def indicator_flip(clauses, assignment, var):
    new_assignment = assignment[:]
    new_assignment[var] = not new_assignment[var]
    return sum(1 for clause in clauses if any(lit in clause for lit in [var, -var]) and all(new_assignment[abs(lit) - 1] == (lit > 0)) for clause in clauses)

def compute_i(g_F):
    n = len(g_F)
    count = 0
    for i in range(1 << n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if g_F[i] != g_F[(i ^ (1 << random.randint(0, n - 1))) % (1 << n)]:
            count += 1
    return count / (1 << n)

def compute_delta(F):
    n = len(F)
    m = sum(len(c) for c in F)
    unsat_count = count_unsat(F)
    i_g_F = compute_i(F)
    if unsat_count == 0:
        return -math.inf
    return math.log2(unsat_count / (1 << n)) - (n * i_g_F) / (2 * unsat_count)

def tree_resolution_depth(F):
    n = len(F)
    memo = {}

    def minimax(clauses, depth=0):
        if not clauses:
            return 0
        key = hash(tuple(sorted(clauses)))
        if key in memo:
            return memo[key]
        min_depth = float('inf')
        for literal in range(n):
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            max_child_depth = 0
            for value in [True, False]:
                new_assignment = [(i >> j) & 1 for j in range(n)]
                new_assignment[literal] = value
                child_clauses = [c for c in new_clauses if any(lit in c for lit in [literal, -literal])]
                max_child_depth = max(max_child_depth, minimax(child_clauses, depth + 1))
            min_depth = min(min_depth, max_child_depth)
        memo[key] = min_depth
        return min_depth

    return minimax(F)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 10, 12, 14, 16]:
        for _ in range(80):
            m = math.floor(4.3 * n)
            clauses = []
            while len(clauses) < m:
                clause = random.sample(range(-n, -1), 3) + random.sample(range(1, n + 1), 3)
                if not is_unsat([clauses]):
                    continue
                clauses.append(clause)
            F = [tuple(sorted(c)) for c in clauses]
            g_F = [is_unsat([c for c in F if literal in c]) for literal in range(1 << n)]
            delta = compute_delta(F)
            d_T = tree_resolution_depth(F)
            results.append((d_T, math.ceil(delta)))
    support_fraction = sum(d >= ceil_delta for d, ceil_delta in results) / len(results)
    mean_slack = sum(max(0, d - ceil_delta) for d, ceil_delta in results) / len(results)
    conjecture_holds = support_fraction >= 0.95 and mean_slack > 0
    counterexample = "" if conjecture_holds else "support_fraction=<{}> mean_slack=<{}>".format(support_fraction, mean_slack)
    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if support_fraction >= 0.95 and mean_slack > 0:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_slack, 0, support_fraction))
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"support_fraction=<{}> mean_slack=<{}>\" first_failing_seed={}".format(support_fraction, mean_slack, first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE support_fraction={} mean_slack={}".format(support_fraction, mean_slack))