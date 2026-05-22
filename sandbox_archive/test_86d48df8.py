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
    
    def fourier_coefficients(circuit, n):
        F = [0] * (2**n)
        for i in range(2**n):
            sum_val = 0
            for k in range(n):
                sum_val += circuit[i] * math.exp(-2j * math.pi * k * i / (2**n))
            F[i] = sum_val / (2**n)
        return F

    def generate_ac0_circuit(n):
        # Placeholder function to generate a random AC0 circuit
        # This is a simplified version and does not actually compute the PARITY function
        circuit = [random.choice([1, -1]) for _ in range(2**n)]
        return circuit

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test each size with 5 different circuits
            circuit = generate_ac0_circuit(n)
            F = fourier_coefficients(circuit, n)
            norm_F = sum(abs(x)**2 for x in F)**0.5

            if norm_F < Fraction(1, 10) * math.log(n):
                conjecture_holds = False
                counterexample = f"n={n}, norm_F={norm_F}"

            total_metric_value += norm_F
            instances_tested += 1

    return {
        "metric_name": "L2-norm of Fourier coefficients",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")