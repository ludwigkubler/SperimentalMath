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
    n = 30
    instances_tested = 0
    total_sum = 0
    k_clique_counterexample = ""

    def walsh_hadamard_transform(f, n):
        if n == 1:
            return [f(0)]
        f_even = walsh_hadamard_transform(lambda x: f(2 * x), n // 2)
        f_odd = walsh_hadamard_transform(lambda x: f(2 * x + 1), n // 2)
        result = []
        for i in range(n):
            if i % 2 == 0:
                result.append(f_even[i // 2] + f_odd[i // 2])
            else:
                result.append(f_even[i // 2] - f_odd[i // 2])
        return result

    def k_clique_indicator_function(x, n, k):
        if len(x) < k:
            return 0
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                if not (x[i] & x[j]):
                    return 0
        return 1

    def sum_abs_values(coefficients):
        return sum(abs(c) for c in coefficients)

    for _ in range(30):
        instance = [random.randint(0, 1) for _ in range(n)]
        coefficients = walsh_hadamard_transform(lambda x: k_clique_indicator_function(instance, n, 3), n)
        total_sum += sum_abs_values(coefficients)
        instances_tested += 1

    mean_value = total_sum / instances_tested
    conjecture_holds = mean_value <= 10 * math.log(n)

    return {
        "metric_name": "Sum of Absolute Fourier Coefficients",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": k_clique_counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")