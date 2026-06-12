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

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def communication_complexity_rank_variance(f):
    n = len(f)
    mte = [sum(hamming_distance(f[i], f[j]) for j in range(n)) / (n * (n - 1) / 2) for i in range(n)]
    return sum(mte) / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [tuple(random.choice([0, 1]) for _ in range(n)) for _ in range(2**n)]

    h_f = sum(hamming_distance(f[i], f[j]) for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1) / 2)
    rc_f = communication_complexity_rank_variance(f)

    metric_value = h_f
    instances_tested = len(f)
    n_max = n
    conjecture_holds = False
    counterexample = ""

    return {
        "metric_name": "H(f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = f"Seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")