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
    
    def fourier_transform(f):
        n = len(f)
        fourier = [0] * n
        for k in range(n):
            term = 0
            for x in range(n):
                if x < n:
                    term += f[x] * (math.cos(2 * math.pi * k * x / n) - 1j * math.sin(2 * math.pi * k * x / n))
                else:
                    break  # Avoid IndexError: list index out of range
            fourier[k] = term
        return fourier
    
    def riemann_zeta(s):
        if s == 1:
            return float('inf')
        zeta = 0
        for k in range(1, 10000):  # Sum a large number of terms to approximate the zeta function
            term = Fraction(1, k**s)
            if abs(term) < 1e-10:
                break
            zeta += term
        return 1 / zeta
    
    def max_entangled_qubits(fourier):
        n = len(fourier)
        entangled_qubits = 0
        for k in range(n):
            if abs(fourier[k]) > 1e-10:
                entangled_qubits += 1
        return entangled_qubits
    
    def taui(fourier):
        n = len(fourier)
        sum_real = 0
        sum_imag = 0
        for k in range(n):
            sum_real += fourier[k].real * math.cos(2 * math.pi * k / n)
            sum_imag += fourier[k].imag * math.sin(2 * math.pi * k / n)
        return Fraction(sum_real, n), Fraction(sum_imag, n)
    
    def inverse_riemann_zeta(s):
        return riemann_zeta(s).inverse()
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = [random.choice([0, 1]) for _ in range(n)]
        fourier = fourier_transform(f)
        tau_real, tau_imag = taui(fourier)
        s = Fraction(1, 2) + tau_real + 1j * tau_imag
        expected_bound = inverse_riemann_zeta(s).real
        actual_bound = max_entangled_qubits(fourier)
        
        total_metric_value += abs(actual_bound - expected_bound)
        instances_tested += n
        
        if abs(actual_bound - expected_bound) > 3:
            conjecture_holds = False
            counterexample = f"n={n}, actual_bound={actual_bound}, expected_bound={expected_bound}"
    
    return {
        "metric_name": "Max Entangled Qubits",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_budget_exceeded")