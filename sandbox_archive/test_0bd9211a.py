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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'x1'
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left}) {op} ({right})'

    def monomial_representation(formula):
        if formula.startswith('(') and formula.endswith(')'):
            formula = formula[1:-1]
        if '&' in formula:
            left, operator, right = formula.split('&', 1)
            return monomial_representation(left) + monomial_representation(right)
        elif '|' in formula:
            left, operator, right = formula.split('|', 1)
            return monomial_representation(left) + monomial_representation(right)
        else:
            return formula

    def lll_reduction(M):
        n = len(M)
        B = M
        G = [Fraction(0)] * n
        U = [[Fraction(0)] * n for _ in range(n)]
        V = [[Fraction(0)] * n for _ in range(n)]

        # Gram-Schmidt process
        for i in range(n):
            B[i] = M[i]
            G[i] = B[i][i].numerator / B[i][i].denominator
            U[0][i] = Fraction(1)
            V[i][0] = B[i][i]

        # LLL reduction
        for k in range(1, n):
            for j in range(k - 1, -1, -1):
                alpha = G[k][j] / G[j][j]
                if abs(alpha) >= Fraction(3, 4):
                    B[k], B[j] = B[j], B[k]
                    U[k], U[j] = U[j], U[k]
                    V[k], V[j] = V[j], V[k]
                    G[k], G[j] = G[j], G[k]
                else:
                    break
            beta = Fraction(1, 2) if k == j + 1 else Fraction(3, 4)
            for i in range(k, n):
                alpha = G[i][k] / G[k][k]
                B[i] -= alpha * B[k]
                U[i][k] -= alpha * U[k][k]
                V[i][k] -= alpha * V[k][k]
                G[i] -= alpha * G[k]

        return B, G

    def resolution_width(formula):
        if formula.startswith('(') and formula.endswith(')'):
            formula = formula[1:-1]
        if '&' in formula:
            left, operator, right = formula.split('&', 1)
            return max(resolution_width(left), resolution_width(right))
        elif '|' in formula:
            left, operator, right = formula.split('|', 1)
            return 1 + max(resolution_width(left), resolution_width(right))
        else:
            return 0

    def min_local_ring_norm(formula):
        M = monomial_representation(formula)
        B, G = lll_reduction([[Fraction(1)] * len(M) for _ in range(len(M))])
        return sum(G[i].numerator / G[i].denominator for i in range(len(G)))

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        min_lrn = min_local_ring_norm(formula)
        w_phi = resolution_width(formula)
        metric_values.append(min_lrn / w_phi)

    if len(metric_values) < 30:
        return {
            "metric_name": "minLRN/w(φ)",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((metric_values[i] - mean_metric) * (i + 1) for i in range(len(metric_values))) / (len(metric_values) * std_metric)

    if correlation_coefficient < 0.8 or not (1 <= mean_metric <= 10):
        conjecture_holds = False
        counterexample = "correlation_threshold_violation"

    return {
        "metric_name": "minLRN/w(φ)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_violation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")