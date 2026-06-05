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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(2 * n, 3 * n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [[0] * (2 ** n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for j in range(1 << n):
                if all((j & (1 << abs(l) - 1)) != 0 == l > 0 for l in clause):
                    poly[i][j] = 1
        return poly

    def min_local_induction_ring_rank(poly):
        n = len(poly[0])
        m = len(poly)
        rank = 0
        while True:
            found = False
            for i in range(m):
                if any(poly[i][j] == 1 for j in range(2 ** n)):
                    rank += 1
                    for j in range(2 ** n):
                        if poly[i][j] == 1:
                            for k in range(n):
                                if (j & (1 << k)) != 0:
                                    poly[i][j ^ (1 << k)] = 0
                    found = True
                    break
            if not found:
                break
        return rank

    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        m = len(cnf)
        rank = 0
        while True:
            found = False
            for i in range(m):
                if any(all((j & (1 << abs(l) - 1)) != 0 == l > 0 for l in clause) for clause in cnf):
                    rank += 1
                    for j in range(2 ** n):
                        if all((j & (1 << abs(l) - 1)) != 0 == l > 0 for l in cnf):
                            for k in range(n):
                                if (j & (1 << k)) != 0:
                                    for clause in cnf:
                                        if (j ^ (1 << k)) not in [sum(2 ** abs(l) - 1 for l in clause) for clause in cnf]:
                                            rank += 1
                    found = True
                    break
            if not found:
                break
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        poly = clause_indicator_polynomial(cnf)
        m_lir = min_local_induction_ring_rank(poly)
        r_Γ = communication_complexity_rank(cnf)
        results.append({"n": n, "m_lir": m_lir, "r_Γ": r_Γ})

    if not results:
        return {
            "metric_name": "m_lir vs r_Γ",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }

    m_lir_values = [result["m_lir"] for result in results]
    r_Γ_values = [result["r_Γ"] for result in results]

    if len(m_lir_values) < 30:
        return {
            "metric_name": "m_lir vs r_Γ",
            "metric_value": None,
            "instances_tested": len(m_lir_values),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean_m_lir = sum(m_lir_values) / len(m_lir_values)
    mean_r_Γ = sum(r_Γ_values) / len(r_Γ_values)

    correlation = 0
    for m, r in zip(m_lir_values, r_Γ_values):
        correlation += (m - mean_m_lir) * (r - mean_r_Γ)
    correlation /= math.sqrt(sum((m - mean_m_lir) ** 2 for m in m_lir_values)) * math.sqrt(sum((r - mean_r_Γ) ** 2 for r in r_Γ_values))

    return {
        "metric_name": "m_lir vs r_Γ",
        "metric_value": correlation,
        "instances_tested": len(m_lir_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")