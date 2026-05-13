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
    
    def free_cumulant(truth_table):
        n = len(truth_table)
        cumulants = [0] * (n + 1)
        for i in range(n):
            for j in range(i, n):
                if truth_table[i][j]:
                    cumulants[j - i + 1] += 1
        return max(cumulants)

    def moment_cumulant_inversion(moments):
        cumulants = [0] * len(moments)
        for k in range(1, len(moments)):
            cumulants[k] = moments[k]
            for j in range(k - 1, 0, -1):
                cumulants[j] -= (j + 1) * cumulants[j + 1]
            cumulants[0] /= k
        return cumulants

    def generate_3sat_instance(n):
        instance = []
        for _ in range(2**n):
            assignment = [random.choice([True, False]) for _ in range(n)]
            clause = random.choice([assignment, [not x for x in assignment]])
            instance.append(clause)
        return instance

    def truth_table(instance):
        n = len(instance[0])
        table = [[False] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            assignment = [bool(i >> j & 1) for j in range(n)]
            for clause in instance:
                if all([assignment[j] or not x for j, x in enumerate(clause)]):
                    table[i][i ^ sum(1 << j for j, x in enumerate(assignment))] = True
        return table

    def read_twice_bp(truth_table):
        n = len(truth_table)
        bp = [[False] * (2**n) for _ in range(2**n)]
        for i in range(n):
            for j in range(2**n):
                if truth_table[i][j]:
                    bp[j][j ^ 1 << i] = True
        return bp

    def cumulants(bp):
        n = len(bp)
        moments = [0] * (n + 1)
        for i in range(n):
            for j in range(i, n):
                if bp[i][j]:
                    moments[j - i + 1] += 1
        return moment_cumulant_inversion(moments)

    def ip2_function():
        bp = [[False] * (2**40) for _ in range(2**40)]
        for i in range(2**40):
            for j in range(i, 2**40):
                if i & j == 0:
                    bp[i][j] = True
        return bp

    n = 40
    instance = generate_3sat_instance(n)
    truth_table_3sat = truth_table(instance)
    cumulant_3sat = free_cumulant(truth_table_3sat)

    ip2_bp = ip2_function()
    cumulants_ip2 = cumulants(ip2_bp)

    max_cumulant_3sat = max(cumulant_3sat)
    max_cumulant_ip2 = max(cumulants_ip2)

    conjecture_holds = max_cumulant_3sat <= 5 * math.log(n) and max_cumulant_ip2 > 40
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "max_free_cumulant",
        "metric_value": max_cumulant_3sat,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")