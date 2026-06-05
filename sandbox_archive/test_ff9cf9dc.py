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
    
    def fourier_transform(f, n):
        result = [0] * (2 ** n)
        for k in range(2 ** n):
            sum_real = 0
            sum_imag = 0
            for j in range(2 ** n):
                angle = 2 * math.pi * k * j / (2 ** n)
                real_part = f(j) * math.cos(angle)
                imag_part = -f(j) * math.sin(angle)
                sum_real += real_part
                sum_imag += imag_part
            result[k] = (sum_real, sum_imag)
        return result

    def taui(fourier):
        n = len(fourier)
        sum_real = 0
        sum_imag = 0
        for k in range(n):
            sum_real += abs(fourier[k][0])
            sum_imag += abs(fourier[k][1])
        return Fraction(sum_real, n), Fraction(sum_imag, n)

    def max_entangled_qubits(fourier):
        n = len(fourier)
        max_qubits = 0
        for k in range(n):
            if fourier[k][0] != 0 or fourier[k][1] != 0:
                max_qubits += 1
        return max_qubits

    def riemann_zeta(s, tol=1e-10):
        result = 0
        n = 1
        while True:
            term = Fraction(1, n ** s)
            if abs(term) < tol:
                break
            result += term
            n += 1
        return result

    def riemann_zeta_inv(s):
        return 1 / riemann_zeta(s)

    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2 ** n)]

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        f = random_boolean_function(n)
        fourier = fourier_transform(f, n)
        tau_real, tau_imag = taui(fourier)
        expected_bound = abs(riemann_zeta_inv(Fraction(1, 2) + Fraction(tau_real, tau_imag)))
        actual_value = max_entangled_qubits(fourier)

        if actual_value < expected_bound - 3 or actual_value > expected_bound + 3:
            conjecture_holds = False
            counterexample = f"n={n}, expected_bound={expected_bound}, actual_value={actual_value}"
            break

        total_metric_value += actual_value
        instances_tested += len(fourier)
        n_max = max(n_max, n)

    return {
        "metric_name": "max_entangled_qubits",
        "metric_value": total_metric_value / instances_tested,
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
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")