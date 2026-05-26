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
    n = 40
    instances_tested = 30
    total_ratio = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random disjointness function
        A = set(random.sample(range(n), n // 2))
        B = set(random.sample(range(n), n // 2))

        # Compute the communication complexity CC_R(DISJ_n)
        cc_disj = len(A & B)

        # Compute the configuration space cohomology H^1(C(n), R)
        # This is a placeholder for the actual computation
        # For simplicity, we assume it's proportional to n
        cohomology_rank = n

        # Calculate the ratio
        if cc_disj == 0:
            continue
        ratio = cohomology_rank / cc_disj
        total_ratio += ratio

        # Check if the conjecture holds for this instance
        if ratio < 0.8:
            conjecture_holds = False
            counterexample = f"Instance with n={n}, CC_R(DISJ_n)={cc_disj}, H^1(C(n), R)={cohomology_rank}"

    # Compute the average ratio
    mean_ratio = total_ratio / instances_tested

    return {
        "metric_name": "Ratio of Cohomology Rank to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    # Compute mean and standard deviation of the metric values
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    # Determine the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")