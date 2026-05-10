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

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    rank = 0
    for row in M:
        if any(row):
            rank += 1
    return rank

def discrepancy(instance, rank):
    n = len(instance)
    max_discrepancy = 0
    for S in range(1 << n):
        satisfied = sum(1 for clause in instance if all(instance[clause][i] == (S >> i) & 1 for i in range(n)))
        discrepancy = abs(satisfied - n)
        if discrepancy > max_discrepancy:
            max_discrepancy = discrepancy
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = random.randint(3, 5)
    n = random.randint(k+1, min(40, 2*k+5))
    instance = []
    for _ in range(n):
        clause = [random.choice([0, 1]) for _ in range(n)]
        if sum(clause) > k:
            instance.append(clause)
    M = [[instance[j][i] for j in range(len(instance))] for i in range(n)]
    rank = gaussian_elimination(M)
    disc = discrepancy(instance, rank)
    return {
        "metric_name": "discrepancy",
        "metric_value": disc,
        "instances_tested": len(instance),
        "conjecture_holds": disc <= 1 / rank * 2,
        "counterexample": "" if disc <= 1 / rank * 2 else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_disc = math.sqrt(sum((r["metric_value"] - mean_disc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_disc} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")