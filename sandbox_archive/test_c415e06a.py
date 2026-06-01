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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        factor = 1 / A[i][i]
        for j in range(n):
            if j != i:
                A[j][i] *= factor
            else:
                A[j][i] = 1
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    return sum(1 for row in A_copy if any(row))

def generate_d_regular_graph(d, n):
    G = [[] for _ in range(n)]
    edges = set()
    while len(edges) < d * n // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
    return G

def tseitin_formula(G):
    n = len(G)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    for u in range(n):
        clause = [literals[u]]
        for v in G[u]:
            clause.append(f'-{literals[v]}')
        clauses.append(clause)
    for u in range(n):
        for v in G[u]:
            clause = [f'-{literals[u]}', literals[v]]
            clauses.append(clause)
    return clauses

def monotone_circuit_complexity(clauses):
    n = len(clauses[0])
    count = 0
    for clause in clauses:
        if all(l.startswith('-') for l in clause):
            continue
        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_sum = 0
    m_complexity_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        G = generate_d_regular_graph(d, n)
        φ_G = tseitin_formula(G)
        min_rank = rank(φ_G)
        m_complexity = monotone_circuit_complexity(φ_G)

        min_rank_sum += min_rank
        m_complexity_sum += m_complexity
        instances_tested += len(φ_G)
        n_max = max(n_max, n)

    mean_min_rank = min_rank_sum / instances_tested
    mean_m_complexity = m_complexity_sum / instances_tested

    r_squared = 1 - (sum((mean_min_rank * x - y) ** 2 for x, y in zip([mean_min_rank] * instances_tested, [mean_m_complexity] * instances_tested))) / sum((x - mean_m_complexity) ** 2 for x in [mean_m_complexity] * instances_tested)

    conjecture_holds = r_squared >= 0.9
    counterexample = "" if conjecture_holds else "R² < 0.9"

    return {
        "metric_name": "min_rank vs m_complexity",
        "metric_value": mean_min_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["r_squared"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='R² < 0.9' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")