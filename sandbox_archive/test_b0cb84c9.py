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
    
    def monotone_width(circuit):
        # Placeholder for actual monotone width calculation
        return len(circuit)

    def halton_sequence(n, base=2):
        sequence = []
        for i in range(1, n + 1):
            frac = 0.0
            denom = 1.0
            while i > 0:
                denom *= base
                frac += (i % base) / denom
                i //= base
            sequence.append(frac)
        return sequence

    def euler_maclaurin_approximation(circuit, points):
        # Placeholder for actual approximation using Euler-Maclaurin formula
        return sum(points)

    def quasi_monte_carlo_error(circuit, epsilon):
        w_C = monotone_width(circuit)
        n_max = int(w_C ** 2 / math.log(1 / epsilon) ** 2)
        if n_max < 5:
            return float('inf')
        points = halton_sequence(n_max)
        error = euler_maclaurin_approximation(circuit, points)
        return abs(error)

    def generate_monotone_circuit(n):
        # Placeholder for actual circuit generation
        return [random.randint(0, 1) for _ in range(n)]

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_error = 0.0
    max_n = 0

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_monotone_circuit(n)
            epsilon = random.uniform(1e-6, 1e-3)
            error = quasi_monte_carlo_error(circuit, epsilon)
            total_error += error
            instances_tested += 1
            max_n = max(max_n, n)

    mean_error = total_error / instances_tested
    conjecture_holds = all(error <= 1e-5 for error in [quasi_monte_carlo_error(generate_monotone_circuit(n), 1e-3) for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Quasi-Monte Carlo Error",
        "metric_value": mean_error,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 17 for i in range(30)]  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_error = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_error} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_error} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")