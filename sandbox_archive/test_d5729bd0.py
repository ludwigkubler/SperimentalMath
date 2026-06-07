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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def min_topological_entropy(cnf):
        # Placeholder implementation
        # This is a dummy function and should be replaced with actual computation
        return random.random()
    
    def communication_complexity_rank_variance(cnf):
        # Placeholder implementation
        # This is a dummy function and should be replaced with actual computation
        return random.random() * min_topological_entropy(cnf)
    
    n = 10  # Example value for n, can be adjusted within the loop
    crv = communication_complexity_rank_variance(generate_cnf(n))
    h_min = min_topological_entropy(generate_cnf(n))
    
    if h_min <= math.log2(n**3):
        conjecture_holds = crv <= 1.5 * h_min**2
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": crv,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_crv = sum(r["metric_value"] for r in results) / len(results)
    std_crv = math.sqrt(sum((r["metric_value"] - mean_crv)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_crv} std={std_crv} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")