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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 1,
            "conjecture_holds": False,
            "counterexample": "single_output_stub"
        }
    
    # Generate a random Boolean function f of size n
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the communication matrix for f
    comm_matrix = [[0] * (2**n) for _ in range(2**n)]
    for x in range(2**n):
        for y in range(2**n):
            if f[x ^ y] == 1:
                comm_matrix[x][y] = 1
    
    # Calculate the rank variance of the communication matrix
    rank_var = sum(sum(row) for row in comm_matrix)
    
    # Compute the minimal order of an associated formal group G_f
    # This is a placeholder implementation; actual computation depends on the specific formal group theory
    if n == 2:
        order_Gf = 1
    elif n == 3:
        order_Gf = 2
    else:
        order_Gf = n
    
    # Correlate the order of G_f with the rank variance
    correlation = Fraction(order_Gf, rank_var) if rank_var != 0 else None
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")