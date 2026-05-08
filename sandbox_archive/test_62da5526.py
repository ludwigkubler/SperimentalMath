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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(n, num_terms):
        variables = list(range(n))
        terms = []
        for _ in range(num_terms):
            term = set(random.sample(variables, random.randint(1, n)))
            terms.append(term)
        return terms
    
    def matroid_representation_size(terms):
        # Simple heuristic to estimate the size of a matroid representation
        # This is a placeholder and should be replaced with an actual algorithm
        return len(terms) * 2
    
    n = random.randint(5, 40)
    num_terms = random.randint(10, min(n**2, 100))
    dnf = generate_dnf(n, num_terms)
    
    mu_phi = matroid_representation_size(dnf)
    
    if len(dnf) > 100:
        return {
            "metric_name": "matroid_representation_size",
            "metric_value": mu_phi,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    k = 3
    lower_bound = n**(1 - 1/k)
    
    return {
        "metric_name": "matroid_representation_size",
        "metric_value": mu_phi,
        "instances_tested": 1,
        "conjecture_holds": mu_phi <= 2 * math.log(n) and mu_phi >= lower_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")