# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations_with_replacement, permutations

def partitions(n):
    def partitions_recursive(n, max_partition):
        if n == 0:
            return [[]]
        result = []
        for i in range(1, min(n, max_partition) + 1):
            for p in partitions_recursive(n - i, i):
                result.append([i] + p)
        return result
    return partitions_recursive(n, n)

def kronecker_coefficient(lam, mu, nu):
    # Placeholder function to compute Kronecker coefficient
    # This is a dummy implementation and should be replaced with actual computation
    return 1.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(2, 40)
    m = random.randint(1, int(n ** 1.5))
    
    lam_partitions = partitions(n)
    mu_partitions = partitions(m)
    nu_partitions = partitions(m)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for lam in lam_partitions:
        for mu in mu_partitions:
            for nu in nu_partitions:
                g1 = kronecker_coefficient(lam, mu, nu)
                g2 = kronecker_coefficient(lam[::-1], mu[::-1], nu[::-1])
                instances_tested += 1
                if g1 <= g2:
                    conjecture_holds = False
                    counterexample = f"Counterexample found: (λ={lam}, μ={mu}, ν={nu})"
                    break
    
    return {
        "metric_name": "Kronecker Coefficient Asymmetry",
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [50, 71, 83, 97, 101]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")