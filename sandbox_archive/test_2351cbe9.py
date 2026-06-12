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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def birational_transformations(G):
    n = len(G)
    A = [[0] * (2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            if G[i][j]:
                A[2*i][2*j] = 1
                A[2*i+1][2*j+1] = 1
                A[2*i][2*j+1] = -1
                A[2*i+1][2*j] = -1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    m_geom_values = []
    w_phi_G_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if not any(sum(row) > 0 for row in G) or not any(sum(col) > 0 for col in zip(*G)):
            continue
        m_geom_G = birational_transformations(G)
        w_phi_G = sum(max(row.count(1), row.count(-1)) for row in G)
        m_geom_values.append(m_geom_G)
        w_phi_G_values.append(w_phi_G)

    if not m_geom_values or not w_phi_G_values:
        return {
            "metric_name": "m_geom(G)",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_m_geom = sum(m_geom_values) / len(m_geom_values)
    std_m_geom = math.sqrt(sum((x - mean_m_geom) ** 2 for x in m_geom_values) / len(m_geom_values))
    correlation_coefficient = (sum((m_geom_values[i] - mean_m_geom) * (w_phi_G_values[i] - sum(w_phi_G_values) / len(w_phi_G_values)) for i in range(len(m_geom_values))) /
                               (len(m_geom_values) * std_m_geom * math.sqrt(sum((x - sum(w_phi_G_values) / len(w_phi_G_values)) ** 2 for x in w_phi_G_values))))

    return {
        "metric_name": "m_geom(G)",
        "metric_value": mean_m_geom,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_m_geom = sum(r["metric_value"] for r in results) / len(results)
    std_m_geom = math.sqrt(sum((r["metric_value"] - mean_m_geom) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_m_geom} std={std_m_geom} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")