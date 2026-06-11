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

def random_kcnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def polynomial_eval(poly, x):
    result = 0
    for coeff in poly:
        term = 1
        for var, exp in coeff.items():
            term *= x ** exp
        result += coeff[0] * term
    return result

def clause_indicator_polynomial(phi, p):
    n = len(phi)
    poly = [{} for _ in range(n)]
    for i in range(n):
        for j in range(len(phi[i])):
            var = abs(phi[i][j])
            exp = phi[i].count(var) - 1
            if var not in poly[i]:
                poly[i][var] = 0
            poly[i][var] += (-1) ** (phi[i][j] > 0)
    for i in range(n):
        for j in range(i + 1, n):
            common_vars = set(poly[i].keys()) & set(poly[j].keys())
            if len(common_vars) == 0:
                continue
            coeff = poly[i][common_vars.pop()]
            for var in common_vars:
                coeff *= poly[j][var]
            poly[i][coeff] += 1
    return poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    h_phi_values = []
    w_phi_values = []

    for n in n_values:
        phi = random_kcnf(n, n * (n - 1) // 2)
        p = random.randint(2, 100)
        h_phi = sum(abs(polynomial_eval(clause_indicator_polynomial(phi, p), x)) for x in range(-n, n+1))
        w_phi = len(phi) * n
        h_phi_values.append(h_phi)
        w_phi_values.append(w_phi)

    mean_h_phi = sum(h_phi_values) / len(h_phi_values)
    std_h_phi = math.sqrt(sum((x - mean_h_phi) ** 2 for x in h_phi_values) / len(h_phi_values))
    ratio_values = [h_phi / w_phi for h_phi, w_phi in zip(h_phi_values, w_phi_values)]
    mean_ratio = sum(ratio_values) / len(ratio_values)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratio_values) / len(ratio_values))

    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(h_phi_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= mean_ratio <= 2 and std_ratio <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")