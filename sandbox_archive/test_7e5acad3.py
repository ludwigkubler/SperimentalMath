# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def minimal_topological_degree(f):
    n = int(f[0].bit_length())
    count = 0
    for i in range(n):
        for j in range(2**n):
            if f[j] != f[j ^ (1 << i)]:
                count += 1
                break
    return Fraction(count, 2**n)

def communication_complexity_rank_variance(f):
    n = int(f[0].bit_length())
    rank = [0] * (2**n)
    for j in range(2**n):
        rank[j] = sum(1 for i in range(n) if f[j] != f[j ^ (1 << i)])
    mean_rank = sum(rank) / len(rank)
    variance = sum((x - mean_rank)**2 for x in rank) / len(rank)
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        td = minimal_topological_degree(f)
        rc = communication_complexity_rank_variance(f)
        if rc == 0:
            return {
                "metric_name": "minimal_topological_degree",
                "metric_value": float(td),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "rc(f) is zero, making the correlation undefined"
            }
        results.append((td, rc))
    td_mean = sum(td for td, _ in results) / len(results)
    rc_mean = sum(rc for _, rc in results) / len(results)
    if td_mean < 0.5 * rc_mean:
        return {
            "metric_name": "minimal_topological_degree",
            "metric_value": float(td_mean),
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"td(f) = {td_mean} < 0.5 * rc(f) = {0.5 * rc_mean}"
        }
    return {
        "metric_name": "minimal_topological_degree",
        "metric_value": float(td_mean),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    td_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(td_values) / len(results)
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(td_values)/len(td_values):.2f} std={(sum((x - sum(td_values)/len(td_values))**2 for x in td_values)/len(td_values))**0.5:.2f} support_fraction={support_fraction:.2f}"
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"td(f) < 0.5 * rc(f)\" first_failing_seed={first_failing_seed}"

    print(RESULT)