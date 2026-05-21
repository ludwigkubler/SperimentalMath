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

def hypergeometric_coefficient(n, k, m):
    if k > n or k > m:
        return 0
    numerator = math.factorial(m) // (math.factorial(k) * math.factorial(m - k))
    denominator = math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
    return numerator / denominator

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        k = min(n // 2, 3)  # Ensure k is at most n/2 and at least 1
        instances_tested = 0
        total_moments = 0.0
        for _ in range(30):  # Test with 30 random instances per size
            m = random.randint(k, n)
            moments = [hypergeometric_coefficient(n, k, m)]
            for i in range(1, k + 2):
                moments.append(moments[-1] * (m - i) / (n - i))
            total_moments += sum(moments)
            instances_tested += 1
        results.append({
            "metric_name": "Sum of Moments",
            "metric_value": total_moments,
            "instances_tested": instances_tested,
            "conjecture_holds": total_moments >= n ** k * math.log(n),
            "counterexample": "" if total_moments >= n ** k * math.log(n) else f"n={n}, k={k}"
        })
    return {
        "seed": seed,
        "metric_name": "Sum of Moments",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")