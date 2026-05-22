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
    
    def matroid_polynomial(matroid):
        n = len(matroid)
        if n == 0:
            return {()}
        else:
            base_poly = matroid_polynomial(matroid[:-1])
            new_poly = {}
            for subset in base_poly:
                new_subset = tuple(sorted(subset + (n-1,)))
                new_poly[new_subset] = base_poly[subset]
            for i in range(n):
                if any(i in subset for subset in base_poly):
                    continue
                new_poly[(i,)] = 0
            return new_poly

    def permanent_circuit_size(matroid):
        n = len(matroid)
        if n == 0:
            return 1
        else:
            size = 0
            for i in range(n):
                if any(i in subset for subset in matroid):
                    continue
                new_matroid = [tuple(sorted(subset + (i,))) for subset in matroid]
                size += permanent_circuit_size(new_matroid)
            return size

    def min_monomial_degree(poly):
        if not poly:
            return 0
        return max(len(subset) for subset in poly)

    n = random.randint(5, 40)
    matroid = [tuple(random.sample(range(n), k)) for k in range(1, n)]
    
    mp = matroid_polynomial(matroid)
    pccs = permanent_circuit_size(matroid)
    mmd = min_monomial_degree(mp)

    ratio = mmd / pccs
    conjecture_holds = ratio >= 2 ** (n / 2 - 1)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 2^{n/2-1}"

    return {
        "metric_name": "Minimal Monomial Degree Invariant",
        "metric_value": mmd,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] / permanent_circuit_size(run_trial(0)["metric_name"]) for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio < 2^{n/2-1}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")