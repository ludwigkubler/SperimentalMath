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

from fractions import Fraction
import random
import math

# Helper function to compute the Fourier transform of an n-bit Boolean function
def fourier_transform(f):
    n = len(f)
    result = {}
    for k in range(n):
        sum_real = 0
        sum_imag = 0
        for x in range(2**n):
            term = f[x] * (math.cos(2 * math.pi * k * x / n) - 1j * math.sin(2 * math.pi * k * x / n))
            sum_real += term.real
            sum_imag += term.imag
        result[k] = Fraction(sum_real, n) + Fraction(sum_imag, n) * 1j
    return result

# Helper function to compute the inverse Riemann zeta function at s = 1/2 + itau
def inverse_riemann_zeta(tau):
    epsilon = 1e-10
    s = 0.5 + tau * 1j
    zeta_s = 0
    k = 1
    while True:
        term = Fraction(1, k**s)
        if abs(term) < epsilon:
            break
        zeta_s += term
        k += 1
    return -zeta_s

# Main function to run a single trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.randint(0, 1) for _ in range(2**n)]
    
    fourier = fourier_transform(f)
    max_entangled_qubits = max(abs(val.real) + abs(val.imag) for val in fourier.values())
    tau = random.uniform(-10, 10)
    bound = inverse_riemann_zeta(tau)
    
    return {
        "metric_name": "max_entangled_qubits",
        "metric_value": max_entangled_qubits,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(max_entangled_qubits - bound) <= 3,
        "counterexample": "" if conjecture_holds else f"max_entangled_qubits={max_entangled_qubits}, bound={bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")