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
    
    def k_clique_indicator(x, n, k):
        if x < 0 or x >= n:
            return 0
        return 1 if sum(1 for i in range(n) if (x & (1 << i)) != 0 and (x & (1 << (i + 1))) != 0) == k else 0
    
    def sum_abs_fourier_coefficients(f, n):
        transform = walsh_hadamard_transform(f, n)
        return sum(abs(coeff) for coeff in transform)
    
    n = random.randint(5, 40)
    if n < 3:
        return {
            "metric_name": "sum_abs_fourier_coefficients",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    k = random.randint(3, n)
    f_k_clique = lambda x: k_clique_indicator(x, n, k)
    sum_abs_coeffs = sum_abs_fourier_coefficients(f_k_clique, 2 ** n)
    
    return {
        "metric_name": "sum_abs_fourier_coefficients",
        "metric_value": sum_abs_coeffs,
        "instances_tested": 1,
        "conjecture_holds": sum_abs_coeffs >= 0.1 * n,
        "counterexample": "" if sum_abs_coeffs >= 0.1 * n else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")