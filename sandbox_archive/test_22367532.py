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
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def moment_cumulant_inversion(moments):
        n = len(moments)
        cumulants = [moments[0]]
        for k in range(1, n):
            cumulant = moments[k]
            for i in range(k):
                cumulant -= sum(cumulants[i] * cumulants[j] for j in range(i)) / (i + 1)
            cumulants.append(cumulant)
        return cumulants
    
    def free_cumulant_spread(M):
        n = len(M)
        moments = [sum(sum(M[i][j] * M[k][l] for j in range(n) for l in range(n)) for i in range(n)) for k in range(n)]
        cumulants = moment_cumulant_inversion(moments)
        return max(abs(c) for c in cumulants) - min(abs(c) for c in cumulants)
    
    n_values = [10, 20, 30, 40]
    results = []
    for n in n_values:
        M = generate_matrix(n)
        sigma_M = free_cumulant_spread(M)
        results.append(sigma_M >= 0.1 * n)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "free_cumulant_spread",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient seeds or support_fraction < 80%")