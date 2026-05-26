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
    n = 40
    k = 3
    random.seed(seed)
    
    # Generate a random k-SAT instance with n variables
    clauses = []
    for _ in range(k * n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    
    # Construct the conflict set
    conflict_set = set()
    for i in range(n):
        for j in range(i + 1, n):
            if any(abs(clause[0]) == i + 1 and abs(clause[1]) == j + 1 for clause in clauses):
                conflict_set.add((i, j))
    
    # Compute the tropicalized Hodge structure (simplified)
    rank = len(conflict_set)
    
    # Calculate the ratio of minimal rank to log(n)
    if n <= 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n must be positive"
        }
    
    ratio = rank / math.log(n)
    
    # Check if the conjecture holds
    if k == 3:
        expected_ratio = math.log(n) / math.log(k)
        lower_bound = expected_ratio * 0.8
        upper_bound = expected_ratio * 1.2
        if lower_bound <= ratio <= upper_bound and rank <= 1.2 * expected_ratio:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = f"Ratio {ratio} out of bounds [{lower_bound}, {upper_bound}] or rank too high"
    else:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined for k != 3"
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")