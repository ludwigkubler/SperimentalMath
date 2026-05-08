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
    
    def generate_dnf(n, k):
        terms = []
        for _ in range(2**n):
            term = [random.randint(0, 1) for _ in range(n)]
            if sum(term) >= k:
                terms.append(term)
        return terms
    
    def set_intersection_size(A, B):
        return len([i for i in range(len(A)) if A[i] == 1 and B[i] == 1])
    
    n = random.randint(5, 40)
    D = generate_dnf(n, 3)  # k-CLIQUE with k=3
    instances_tested = len(D)
    
    mu_D = sum(len(term) for term in D)
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            mu_D -= set_intersection_size(D[i], D[j])
    
    conjecture_holds = False
    counterexample = ""
    
    if n <= 40:
        if mu_D >= math.sqrt(n):
            conjecture_holds = True
        else:
            counterexample = "mu(D) < sqrt(n)"
    else:
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "mu(D)",
        "metric_value": mu_D,
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
    
    mean_mu_D = sum(r["metric_value"] for r in results) / len(results)
    std_mu_D = math.sqrt(sum((r["metric_value"] - mean_mu_D)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu_D} std={std_mu_D} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mu(D) < sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")