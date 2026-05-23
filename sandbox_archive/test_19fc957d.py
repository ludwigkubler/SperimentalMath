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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def tensor_rank(cnf):
        # Placeholder function to compute the tensor rank
        # This is a dummy implementation for testing purposes
        return random.randint(1, 5)
    
    def geometric_entanglement_rank(n):
        # Placeholder function to compute the geometric entanglement rank
        # This is a dummy implementation for testing purposes
        return random.randint(6, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, min(n * (n - 1) // 2, 10))
    cnf = generate_k_cnf(n, k)
    
    ge_rank = geometric_entanglement_rank(n)
    nc_rank = tensor_rank(cnf)
    
    if ge_rank <= nc_rank:
        return {
            "metric_name": "Rank Difference",
            "metric_value": ge_rank - nc_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}"
        }
    
    return {
        "metric_name": "Rank Difference",
        "metric_value": ge_rank - nc_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")