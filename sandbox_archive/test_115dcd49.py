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

import math
import random
from fractions import Fraction

def hook_length_formula(n, partition):
    total = 1
    for i in range(n):
        for j in range(len(partition)):
            if partition[j] == 0:
                continue
            total *= (n - i + j) / (partition[j] * (i + j))
            partition[j] -= 1
    return total

def multiplicity(n, partition):
    sym_multiplicity = hook_length_formula(n, partition[:]) / math.factorial(n)
    antisym_multiplicity = hook_length_formula(n, partition[:]) / math.factorial(n)
    return sym_multiplicity, antisym_multiplicity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n < 2:
            continue
        sym_multiplicity, antisym_multiplicity = multiplicity(n, (n-1, 1))
        results.append((sym_multiplicity, antisym_multiplicity))
    
    if not results:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    sym_total = sum(result[0] for result in results)
    antisym_total = sum(result[1] for result in results)
    mean_sym = sym_total / len(results)
    mean_antisym = antisym_total / len(results)
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": mean_sym - mean_antisym,
        "instances_tested": len(results),
        "conjecture_holds": mean_sym > mean_antisym,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity gap does not hold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support for conjecture")