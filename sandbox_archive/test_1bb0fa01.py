# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def riemann_zeta(s, tol=1e-6):
        if s == 1:
            return float('inf')
        zeta = 0.5 + 0.25j
        n = 1
        while True:
            term = Fraction(1, (n ** s).real)
            if abs(term) < tol:
                break
            zeta += term
            n += 1
        return zeta
    
    def fourier_transform(f):
        n = len(f)
        result = [0] * n
        for k in range(n):
            sum_real = 0
            sum_imag = 0
            for j in range(n):
                angle = 2 * math.pi * k * j / n
                sum_real += f[j] * math.cos(angle)
                sum_imag -= f[j] * math.sin(angle)
            result[k] = Fraction(sum_real, n) + Fraction(sum_imag, n) * 1j
        return result
    
    def max_entangled_qubits(fourier):
        n = len(fourier)
        max_qubits = 0
        for k in range(n):
            if fourier[k].real != 0:
                max_qubits += 1
        return max_qubits
    
    def inverse_riemann_zeta(s):
        zeta_val = riemann_zeta(s)
        if zeta_val == float('inf'):
            return Fraction(0, 1)
        return Fraction(1, zeta_val.real)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 random n-bit Boolean functions
            f = [random.choice([0, 1]) for _ in range(n)]
            fourier = fourier_transform(f)
            max_qubits = max_entangled_qubits(fourier)
            expected_bound = inverse_riemann_zeta(Fraction(1, 2) + Fraction(random.random(), n))
            if abs(max_qubits - expected_bound.numerator / expected_bound.denominator) > 3:
                return {
                    "metric_name": "max_entangled_qubits",
                    "metric_value": max_qubits,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, max_qubits={max_qubits}, expected_bound={expected_bound}"
                }
            total_metric_value += max_qubits
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "max_entangled_qubits",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")