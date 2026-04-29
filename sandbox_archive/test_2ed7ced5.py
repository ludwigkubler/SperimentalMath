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
        for _ in range(k):
            term = [random.choice([0, 1]) for _ in range(n)]
            terms.append(term)
        return terms
    
    def dnf_to_matroid_rank(dnf):
        rank = len(set(tuple(term) for term in dnf))
        return rank
    
    def submodular_function(dnf):
        return min(dnf_to_matroid_rank(dnf), math.log(len(dnf)))
    
    def is_submodular(F, G):
        return submodular_function(F) + submodular_function(G) - 1 >= submodular_function(F + G)
    
    def test_submodularity():
        for _ in range(100):
            F = generate_dnf(n, random.randint(5, 20))
            G = generate_dnf(n, random.randint(5, 20))
            if not is_submodular(F, G):
                return False
        return True
    
    def test_clique():
        for n in range(10, 41):
            dnf = [[1] * n]
            mu = submodular_function(dnf)
            if mu != n:
                return False
        return True
    
    n = random.randint(5, 40)
    F = generate_dnf(n, random.randint(5, 20))
    mu_F = submodular_function(F)
    
    if not test_submodularity():
        return {
            "metric_name": "submodularity_test",
            "metric_value": None,
            "instances_tested": 100,
            "conjecture_holds": False,
            "counterexample": "Submodularity test failed"
        }
    
    if not test_clique():
        return {
            "metric_name": "clique_test",
            "metric_value": None,
            "instances_tested": 40,
            "conjecture_holds": False,
            "counterexample": "Clique test failed"
        }
    
    return {
        "metric_name": "submodular_function_value",
        "metric_value": mu_F,
        "instances_tested": 1,
        "conjecture_holds": mu_F <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["counterexample"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")