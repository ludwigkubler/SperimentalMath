# auto-injected by SEC sandbox
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
import math
from itertools import combinations

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
    total_sym_multiplicity = 0
    total_antisym_multiplicity = 0
    instances_tested = 0

    for n in n_values:
        sym_multiplicity, antisym_multiplicity = multiplicity(n, (n-1, 1))
        if sym_multiplicity == 0 or antisym_multiplicity == 0:
            continue
        total_sym_multiplicity += sym_multiplicity
        total_antisym_multiplicity += antisym_multiplicity
        instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    sym_multiplicity_avg = total_sym_multiplicity / instances_tested
    antisym_multiplicity_avg = total_antisym_multiplicity / instances_tested

    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": sym_multiplicity_avg - antisym_multiplicity_avg,
        "instances_tested": instances_tested,
        "conjecture_holds": sym_multiplicity_avg > antisym_multiplicity_avg,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity gap does not hold\" first_failing_seed={first_failing_seed}")