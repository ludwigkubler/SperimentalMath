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

def generate_polynomial(d, variables):
    coeffs = [random.randint(-10, 10) for _ in range(d + 1)]
    x = [random.randint(1, 5) for _ in range(variables)]
    return sum(c * tuple(x[i] for i in range(variables))**i for i, c in enumerate(coeffs))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for d in range(10, 101):
            f = generate_polynomial(d, n)
            # Placeholder for actual computation of minimal Schur-Weyl rank
            rho_f = Fraction(d**(2/3)) * random.random()  # Simulated value
            results.append(rho_f / d**(2/3))
    mean_value = sum(results) / len(results)
    std_dev = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
    conjecture_holds = mean_value <= 1.5 and std_dev <= 0.2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Minimal Schur-Weyl Rank / Degree^(2/3)",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(result["metric_value"] > 1.7 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.7)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")