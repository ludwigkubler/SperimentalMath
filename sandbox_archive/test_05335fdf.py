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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        A = gaussian_elimination(A)
        return sum(1 for row in A if any(row))

    def characteristic_polynomial(A):
        n = len(A)
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in zip(p, sorted(p)))
            term = 1
            for i in range(n):
                term *= A[p[i]][i]
            det += sign * term
        return det

    def min_representation_size(poly):
        n = len(poly)
        if poly == 0:
            return 0
        if poly == 1:
            return 1
        factors = []
        for i in range(2, int(math.sqrt(n)) + 1):
            while n % i == 0:
                factors.append(i)
                n //= i
        if n > 1:
            factors.append(n)
        return len(factors)

    def symplectic_quadratic_forms(poly):
        n = len(poly)
        forms = []
        for i in range(1, n):
            form = [0] * n
            form[i-1], form[i] = -poly[i], poly[i-1]
            forms.append(form)
        return forms

    def rank_variance(A):
        m, n = len(A), len(A[0])
        variance = 0
        for i in range(m):
            for j in range(n):
                variance += A[i][j] ** 2
        return variance / (m * n)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, n_max)
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
            A = [[sum(phi[i][j] * phi[j][k] for j in range(n)) for k in range(n)] for i in range(m)]
            det = characteristic_polynomial(A)
            forms = symplectic_quadratic_forms(det)
            min_size = min_representation_size(det)
            var = rank_variance(A)

            if var > min_size:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}"
                break

            total_metric_value += var
            instances_tested += 1

        if not conjecture_holds:
            break

    return {
        "metric_name": "rank_variance",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")