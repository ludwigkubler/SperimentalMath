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
    
    def parity(n, x):
        return sum(int(bit) for bit in bin(x)[2:]) % 2
    
    def noncommutative_fourier_transform(n):
        transform = [0] * (1 << n)
        for i in range(1 << n):
            transform[i] = parity(n, i)
        return transform
    
    def count_nonzero_coefficients(transform):
        return sum(abs(coeff) > 1e-9 for coeff in transform)
    
    d = random.randint(2, 5)
    n = random.randint(5, 40)
    transform = noncommutative_fourier_transform(n)
    nonzero_count = count_nonzero_coefficients(transform)
    expected_lower_bound = math.ceil(n ** (1 / (d - 1)))
    
    return {
        "metric_name": "nonzero_coefficient_count",
        "metric_value": nonzero_count,
        "instances_tested": 1,
        "conjecture_holds": nonzero_count >= expected_lower_bound,
        "counterexample": "" if nonzero_count >= expected_lower_bound else f"n={n}, d={d}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")