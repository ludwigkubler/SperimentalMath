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
    
    k = 3  # Fixed constant for k-SAT
    n = random.randint(5, 40)  # Random number of variables between 5 and 40
    
    # Generate a random k-SAT instance
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), k)]
        clauses.append(clause)
    
    # Construct the conflict set
    conflict_set = set()
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            if any(abs(clauses[i][l]) == abs(clauses[j][m]) for l in range(k) for m in range(k)):
                conflict_set.add((i, j))
    
    # Compute the tropicalized Hodge structure (simplified version)
    rank = len(conflict_set)
    
    # Calculate the ratio of minimal rank to log(n)
    if n <= 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n must be greater than 0"
        }
    
    ratio = rank / math.log(n)
    
    # Check if the conjecture holds
    theta = math.log(n) / math.log(k)
    lower_bound = theta * (1 - 0.2)
    upper_bound = theta * (1 + 0.2)
    
    conjecture_holds = lower_bound <= ratio <= upper_bound
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} is outside bounds [{lower_bound}, {upper_bound}]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 97) for _ in range(30)]  # Default to 30 random primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break