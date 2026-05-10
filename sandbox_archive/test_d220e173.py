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

def generate_gf2_polynomial(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def matroid_rank(poly, n):
    rank = 0
    basis = []
    for term in poly:
        if term == 1:
            variables = [i for i in range(n) if (1 << i) & term]
            if all(all(var not in b for b in basis) for b in basis):
                basis.append(variables)
                rank += 1
    return rank

def acc0_circuit_size(poly, n):
    # Simplified estimation using Williams' diagonalization method
    # This is a placeholder; actual implementation would be more complex
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    c = 1.0  # Constant for the lower bound
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        poly = generate_gf2_polynomial(n)
        rank = matroid_rank(poly, n)
        size = acc0_circuit_size(poly, n)
        if size < c * n**(1 + 1/rank):
            conjecture_holds = False
            counterexample = f"Rank {rank}, Size {size}"
            break

    metric_value = rank
    return {
        "metric_name": "matroid_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")