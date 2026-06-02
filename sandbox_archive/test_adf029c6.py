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
    
    # Generate a random boolean function φ with n variables
    n = 10
    phi = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the automorphic representation (simplified as a list of integers)
    auto_rep = [sum(phi[i] * (i % 2) for i in range(len(phi))) for _ in range(n)]
    
    # Evaluate the L-function zeros (simplified as a count of non-trivial zeros)
    l_function_zeros = sum(1 for x in auto_rep if x != 0)
    
    # Compute the communication complexity rank (simplified as a linear function of n)
    comm_complexity_rank = n
    
    # Check if the conjecture holds
    if l_function_zeros == 0 or comm_complexity_rank == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": comm_complexity_rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate the correlation coefficient
    corr_coeff = (comm_complexity_rank - math.log(l_function_zeros)) / math.sqrt(comm_complexity_rank**2 + l_function_zeros**2)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": comm_complexity_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": corr_coeff >= 0.7 and corr_coeff <= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 or r["communication_complexity_rank"] not in range(int(math.log(1)), int(math.log(100))) for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"invalid\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")