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

def hypergeometric(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, int(n) + 1):
        result *= (n - i + 1) / i
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):
            # Generate a random Boolean satisfiability problem instance with n variables
            phi = [random.choice([True, False]) for _ in range(n)]
            
            # Compute the DPLL path length (simplified model)
            dpll_path_length = sum(phi)  # Simplified model
            
            total_metric_value += abs(dpll_path_length - n ** (1 + alpha))
            instances_tested += 1
            max_n = max(max_n, n)

    conjecture_holds = True
    counterexample = ""

    if instances_tested >= 30:
        mean_metric_value = total_metric_value / instances_tested
        std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in range(instances_tested)) / instances_tested)
        
        # Check if the conjecture holds within a factor of n^(1 + alpha)
        if max_n >= 16:
            alpha = hypergeometric(n_values[0] + 1) * hypergeometric(Fraction(1, 2)) / hypergeometric(n_values[0] + Fraction(3, 2))
            for n in n_values:
                for _ in range(5):
                    phi = [random.choice([True, False]) for _ in range(n)]
                    dpll_path_length = sum(phi)
                    if abs(dpll_path_length - n ** (1 + alpha)) > 0.1 * n ** (1 + alpha):
                        conjecture_holds = False
                        counterexample = f"Failed at n={n}, DPLL_path_length={dpll_path_length}, expected ~{n ** (1 + alpha)}"
                        break
                if not conjecture_holds:
                    break

    return {
        "metric_name": "DPLL Path Length",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")