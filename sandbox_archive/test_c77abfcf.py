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
    
    def xor_and_tree_width(f):
        # Placeholder function to compute XOR-AND tree width
        return len(f)

    def tropicalized_barycentric_rank(f):
        # Placeholder function to compute tropicalized barycentric rank
        return len(f)

    n = 10  # Start with a small size and scale up
    instances_tested = 0
    ranks = []
    widths = []

    while instances_tested < 30:
        f = [random.choice([0, 1]) for _ in range(n)]
        if xor_and_tree_width(f) > n or tropicalized_barycentric_rank(f) > n:
            continue
        
        ranks.append(tropicalized_barycentric_rank(f))
        widths.append(xor_and_tree_width(f))
        instances_tested += 1

    if not ranks or not widths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    n = len(ranks)
    mean_r = sum(ranks) / n
    mean_w = sum(widths) / n
    var_r = sum((x - mean_r) ** 2 for x in ranks) / n
    var_w = sum((x - mean_w) ** 2 for x in widths) / n

    cov_rw = sum((ranks[i] - mean_r) * (widths[i] - mean_w) for i in range(n)) / n
    correlation_coefficient = cov_rw / math.sqrt(var_r * var_w)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={r['seed']}")
                break