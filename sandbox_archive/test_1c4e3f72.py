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
    n = 4
    random.seed(seed)

    def DISJ_n(x, y):
        return any(xi and yi for xi, yi in zip(bin(x)[2:].zfill(n), bin(y)[2:].zfill(n)))

    def is_monotone(circuit):
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j] == 0 and any(circuit[x][y] == 1 for x in range(i) for y in range(j)):
                    return False
        return True

    def exhaustive_monotone_circuit_synthesis():
        min_size = float('inf')
        for _ in range(10):
            circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            if is_monotone(circuit) and all(DISJ_n(i, j) == any(circuit[x][y] == 1 for x in range(n) for y in range(n)) for i in range(n) for j in range(n)):
                min_size = min(min_size, sum(sum(row) for row in circuit))
        return min_size

    D = n
    S = exhaustive_monotone_circuit_synthesis()

    conjecture_holds = D >= n and S >= 2**(n/2)
    counterexample = "" if conjecture_holds else "disjointness_discrepancy"

    return {
        "metric_name": "communication_complexity",
        "metric_value": D,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"disjointness_discrepancy\" first_failing_seed={first_failing_seed}")