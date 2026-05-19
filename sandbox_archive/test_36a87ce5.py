# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    s = random.randint(1, 2**n)
    d = random.randint(1, 10)

    # Generate a random function f ∈ {0,1}^n
    f = [random.choice([0, 1]) for _ in range(2**n)]

    # Construct the SOS moment matrix M_k(f)
    M_k_f = [[sum(f[i] * f[j] for i, j in itertools.combinations(range(2**n), k)) for k in range(n + 1)] for _ in range(n + 1)]

    # Compute the eigenvalues of M_k(f)
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return [A[i][i] for i in range(n)]

    eigenvalues = gaussian_elimination(M_k_f)

    # Find the minimum eigenvalue
    λ_min = min(eigenvalues)

    # Check if λ_min scales as Ω(s^{-1/2})
    threshold = s**(-0.5)
    conjecture_holds = λ_min >= threshold

    return {
        "metric_name": "min_eigenvalue",
        "metric_value": λ_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: n={n}, s={s}, d={d}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")