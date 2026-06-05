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
    
    def generate_tseitin_formula(n, d):
        if n % d != 0:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [i]
            for j in range(d - 1):
                k = random.choice(variables)
                if k != i:
                    clause.append(-k)
                    variables.remove(k)
            clauses.append(clause)
        return clauses

    def gaussian_elimination(A, b):
        n = len(b)
        A_b = [row + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
            pivot = A_b[i][i]
            if pivot == 0:
                return None
            for j in range(n):
                A_b[i][j] /= pivot
            b[i] /= pivot
            for k in range(n):
                if k != i:
                    factor = A_b[k][i]
                    for j in range(n):
                        A_b[k][j] -= factor * A_b[i][j]
                    b[k] -= factor * b[i]
        return [row[-1] for row in A_b]

    def resolution_width(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            if not any(abs(lit) == abs(stack[-1]) for lit in clause):
                stack.append(clause[0])
            else:
                stack.pop()
                clauses.extend([c for c in clauses if c and all(lit not in c for lit in clause)])
        return len(stack)

    n_max = 40
    instances_tested = 0
    OHD_values = []
    w_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 10))
            formula = generate_tseitin_formula(n, d)
            if formula is None:
                continue
            A = [[0] * n for _ in range(n)]
            b = [0] * n
            for clause in formula:
                for lit in clause:
                    i = abs(lit) - 1
                    if lit > 0:
                        A[i][i] += 1
                    else:
                        A[i][i] -= 1
                    b[i] += 1 if lit > 0 else -1
            OHD = gaussian_elimination(A, b)
            if OHD is None:
                continue
            w = resolution_width(formula)
            OHD_values.append(OHD)
            w_values.append(w)
            instances_tested += 1

    if not OHD_values or not w_values:
        return {
            "metric_name": "OHD vs w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    OHD_mean = sum(OHD_values) / len(OHD_values)
    w_mean = sum(w_values) / len(w_values)
    correlation = sum((OHD - OHD_mean) * (w - w_mean) for OHD, w in zip(OHD_values, w_values)) / (len(OHD_values) * math.sqrt(sum((OHD - OHD_mean) ** 2 for OHD in OHD_values) * sum((w - w_mean) ** 2 for w in w_values)))
    max_OHD = max(OHD_values)
    conjecture_holds = correlation >= 0.8 and max_OHD <= 3 * w_mean

    return {
        "metric_name": "OHD vs w",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_OHD={max_OHD}, 3*w_mean={3 * w_mean}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")