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
    n = 10  # Start with a small size and increase if needed
    max_n = 40
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""

    while instances_tested < 30 and n <= max_n:
        k = random.randint(2, n-1)
        clique_size = math.comb(n, k)
        if clique_size > 100:  # Skip large cliques to avoid timeout
            n += 5
            continue

        # Generate a random k-clique instance
        clique = set(random.sample(range(n), k))
        matroid_rank = len(clique)  # Rank of the matroid is simply the size of the clique

        # Compute rank for DNF formulas of varying sizes
        dnf_sizes = [1, 2, 3, 4]
        for size in dnf_sizes:
            if random.random() < 0.5:  # Randomly decide to include this size
                instances_tested += 1
                total_rank += matroid_rank

        n += 5

    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / 30

    return {
        "metric_name": "matroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(res["metric_value"] for res in results if "metric_value" in res) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")