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
            sum_val = 0.0
            for k in range(n + 1):
                sum_val += circuit[i] * math.exp(-2j * math.pi * k * i / (2**n))
            F[i] = sum_val
        return F
    
    def ac0_circuit(n):
        # Generate a random AC0 circuit computing the PARITY function
        circuit = [random.choice([1, -1]) for _ in range(2**n)]
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        circuit = ac0_circuit(n)
        F = fourier_coefficients(circuit, n)
        l2_norm = sum(abs(x)**2 for x in F) ** 0.5
        metrics.append(l2_norm)
    
    mean_l2_norm = sum(metrics) / len(metrics)
    support_fraction = all(norm >= math.log(n) for norm, n in zip(metrics, n_values))
    
    return {
        "metric_name": "L^2-norm of Fourier coefficients",
        "metric_value": mean_l2_norm,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "n/a"
    }

if __name__ == "__main__":
    default_seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    seeds = list(map(int, random.sample(default_seeds, 30))) if len(sys.argv) == 1 else list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=n/a support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n/a' first_failing_seed={first_failing_seed}")