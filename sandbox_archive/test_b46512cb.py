# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = -1
        for i in range(rank, rows):
            if matrix[i][j] == 1:
                i_max = i
                break
        if i_max >= 0:
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for k in range(j + 1, cols):
                matrix[rank][k] ^= matrix[rank][j]
            rank += 1
    return rank

def bdd_width(truth_table):
    n = len(truth_table)
    if n == 0:
        return 0
    variables = list(range(n))
    width = 0
    while variables:
        var = random.choice(variables)
        variables.remove(var)
        new_vars = []
        for i in range(1 << (n - 1)):
            x = [bool((i >> j) & 1) for j in range(n)]
            if truth_table[i][var] != truth_table[2 * i][var]:
                new_vars.append(var)
                break
        width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    M_f = [[random.randint(0, 1) for _ in range(2**n)] for _ in range(n)]
    rank = gaussian_elimination(M_f)
    bdd_width_value = bdd_width(M_f)
    conjecture_holds = rank <= bdd_width_value
    counterexample = "" if conjecture_holds else "bdd_width < rank"
    return {
        "metric_name": "rank vs. BDD width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"bdd_width < rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")