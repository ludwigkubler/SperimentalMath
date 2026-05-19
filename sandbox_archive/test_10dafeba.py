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
    
    def hook_length_formula(n, partition):
        total = 1
        for i in range(n):
            for j in range(len(partition)):
                if partition[j] == 0:
                    break
                total *= (n - i + j) / (partition[j] * (i + j))
                partition[j] -= 1
        return total
    
    def minor(m, n, k):
        if m == 1 and n == 1:
            return 1
        det = 0
        for a in range(1, m + 1):
            sign = (-1) ** (a % 2)
            sub_minor = minor(m - 1, n - 1, k - 1 if a <= k else k)
            det += sign * a * sub_minor
        return det
    
    def schur_elementary(n, b):
        return sum((-1)**(a - b - k) * minor(a - b - k, k, b) for k in range(b + 1))
    
    def schur_polynomial(n, partition):
        det = 1
        for i in range(len(partition)):
            det *= schur_elementary(n - partition[i], i)
        return det
    
    def multiplicity(n, partition):
        sym_multiplicity = hook_length_formula(n, partition) / math.factorial(n)
        antisym_multiplicity = hook_length_formula(n, partition) / math.factorial(n)
        return sym_multiplicity, antisym_multiplicity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sym_multiplicity, antisym_multiplicity = multiplicity(n, (n-1, 1))
        results.append((sym_multiplicity, antisym_multiplicity))
    
    mean_sym = sum(x[0] for x in results) / len(results)
    mean_antisym = sum(x[1] for x in results) / len(results)
    
    if mean_sym <= mean_antisym:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": mean_sym - mean_antisym,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": f"n={n}, sym_multiplicity={mean_sym}, antisym_multiplicity={mean_antisym}"
        }
    else:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": mean_sym - mean_antisym,
            "instances_tested": len(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity Gap\" first_failing_seed={first_failing_seed}")