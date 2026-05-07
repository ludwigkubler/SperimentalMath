# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
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

def dpll(f):
    if not f:
        return True
    for literal in f[0]:
        new_f = [clause for clause in f if literal not in clause and -literal not in clause]
        if dpll(new_f):
            return True
    return False

def is_unsat(f):
    return not dpll(f)

def random_3cnf(n, m):
    clauses = []
    variables = set(range(1, n + 1))
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.choice(list(variables))
            polarity = random.choice([True, False])
            if polarity:
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def build_dag(f):
    n = len(f)
    m = sum(len(clause) for clause in f)
    adj_list = [[] for _ in range(m)]
    topological_order = []
    visited = [False] * m
    stack = []

    def dfs(v):
        if not visited[v]:
            visited[v] = True
            for u in adj_list[v]:
                dfs(u)
            stack.append(v)

    for i, clause in enumerate(f):
        for literal in clause:
            for j, other_clause in enumerate(f):
                if i != j and any(l == -o for l, o in zip(clause, other_clause)):
                    adj_list[i].append(j)

    while stack:
        v = stack.pop()
        topological_order.append(v)

    return adj_list, topological_order

def greedy_morse_matching(adj_list, topological_order):
    n = len(adj_list)
    matched_edges = [False] * n
    critical_edges = 0

    for v in reversed(topological_order):
        if not matched_edges[v]:
            for u in adj_list[v]:
                if not matched_edges[u]:
                    matched_edges[u] = True
                    break
            else:
                critical_edges += 1

    return critical_edges

def frege_depth(f, topological_order):
    n = len(topological_order)
    depth = [0] * n
    for v in reversed(topological_order):
        max_depth = 0
        for u in adj_list[v]:
            if not matched_edges[u]:
                max_depth = max(max_depth, depth[u])
        depth[v] = max_depth + 1

    return max(depth)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [10, 15, 20, 25, 30, 40]:
        m = math.floor(4.5 * n)
        count = 0
        while count < 30:
            f = random_3cnf(n, m)
            if is_unsat(f):
                adj_list, topological_order = build_dag(f)
                critical_edges = greedy_morse_matching(adj_list, topological_order)
                d_pi = frege_depth(f, topological_order)
                results.append((n, critical_edges, d_pi))
                count += 1

        M_F = sum(critical_edges for _, critical_edges, _ in results) / len(results)
        log_n_over_log_n = math.log(n / math.log(n)) if n > 0 else 0
        log_M_F = math.log(M_F) if M_F > 0 else 0

        per_instance_bound_holds = all(critical_edges >= d_pi - math.ceil(math.log2(len(adj_list))) for _, critical_edges, d_pi in results)
        ols_slope = (log_M_F * len(results) - sum(log_n_over_log_n * log_M_F for n, M_F, _ in results)) / (len(results) ** 2)

        conjecture_holds = per_instance_bound_holds and 0.8 <= ols_slope <= 1.2
        counterexample = "" if conjecture_holds else "mapping_undefined"

        return {
            "metric_name": "M(F)",
            "metric_value": M_F,
            "instances_tested": len(results),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*40+2))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_M_F = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_M_F) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_M_F} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data to draw a conclusion")