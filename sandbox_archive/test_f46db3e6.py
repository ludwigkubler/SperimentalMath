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
    
    def generate_dnf(m: int, n: int):
        dnf = []
        for _ in range(m):
            term = [random.randint(0, 1) for _ in range(n)]
            dnf.append(term)
        return dnf
    
    def euclidean_distance(x, y):
        return sum((xi - yi) ** 2 for xi, yi in zip(x, y))
    
    def dispersion(dnf):
        n = len(dnf[0])
        max_dist_squared = 0
        for i in range(len(dnf)):
            for j in range(i + 1, len(dnf)):
                dist_squared = euclidean_distance(dnf[i], dnf[j])
                if dist_squared > max_dist_squared:
                    max_dist_squared = dist_squared
        return max_dist_squared
    
    n_max = 40
    m_max = 40
    instances_tested = 30
    metric_name = "dispersion"
    
    results = []
    for _ in range(instances_tested):
        m = random.randint(5, min(m_max, n_max))
        dnf = generate_dnf(m, n_max)
        mu = dispersion(dnf)
        results.append(mu)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    conjecture_holds = all(mu <= 5 * math.log(m) for m, mu in zip([m] * instances_tested, results))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no seeds tested")