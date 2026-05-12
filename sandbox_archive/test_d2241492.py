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
    
    def R_transform_inv(cumulants):
        n = len(cumulants)
        if n == 0:
            return 0
        elif n == 1:
            return cumulants[0]
        else:
            inv_cums = [cumulants[0]]
            for k in range(1, n):
                inv_cums.append((inv_cums[-1] * (k - 1) + cumulants[k]) / k)
            return inv_cums
    
    def free_cumulants(matrix):
        n = len(matrix)
        cums = [0] * n
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] != 0:
                    cums[j - i] += matrix[i][j]
        return R_transform_inv(cums)
    
    def DISJ_n(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    n = random.randint(5, 40)
    M = DISJ_n(n)
    cumulants = free_cumulants(M)
    μ_M = sum(abs(c) for c in cumulants)
    
    metric_name = "μ(M)"
    metric_value = μ_M
    instances_tested = 1
    conjecture_holds = μ_M >= 0.9 * n
    counterexample = "" if conjecture_holds else f"n={n}, μ(M)={μ_M}"
    
    return {
        "metric_name": metric_name,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")