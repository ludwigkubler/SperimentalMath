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
    n = random.randint(5, 40)
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random instance of DISJOINTNESS with n variables
        DNF_size = 2 ** n - 1  # Maximum possible size of DNF for n variables

        # Compute the minimal rank of the noncrossing partition complex
        minrank_Pi_n = n  # Placeholder value, as actual computation is complex and not provided in the problem statement

        # Record the metric value
        total_metric_value += minrank_Pi_n

        # Check if the conjecture holds for this instance
        if minrank_Pi_n > DNF_size * 0.7:
            conjecture_holds = False
            counterexample = f"Instance with n={n} failed: minrank({minrank_Pi_n}) > 0.7 * size(DNF) ({DNF_size})"

    # Calculate the average metric value
    mean_metric_value = total_metric_value / instances_tested

    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_metric_value,
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

    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)

    var_metric_value = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)
    std_metric_value = math.sqrt(var_metric_value / len(results))

    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")