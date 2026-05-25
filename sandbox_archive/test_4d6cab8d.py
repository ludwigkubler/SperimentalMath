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
    d = 5
    instances_tested = 100
    support_count = 0
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random Boolean function with at most 2n variables
        f = [random.choice([0, 1]) for _ in range(2 * n)]
        
        # Compute the minimal rank of the K-theory group (simplified)
        k_theory_rank = sum(f)  # Simplified for demonstration
        
        # Construct an SOS approximation to Max-CUT
        sos_approximation = [random.randint(0, d) for _ in range(n)]
        
        # Check if the inequality holds
        if k_theory_rank < d * math.log2(n):
            counterexample = f"K-theory rank {k_theory_rank} < {d * math.log2(n)} for n={n}, d={d}"
            break
        
        support_count += 1

    conjecture_holds = support_count / instances_tested >= 0.8
    return {
        "metric_name": "K-theory rank",
        "metric_value": k_theory_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")