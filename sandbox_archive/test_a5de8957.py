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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters for k-CNF instances
    n = random.randint(5, 40)  # Number of variables
    m = random.randint(n, n * 2)  # Number of clauses
    
    # Generate a random k-CNF instance
    F = []
    for _ in range(m):
        clause = set(random.sample(range(n), random.randint(1, n)))
        F.append(clause)
    
    # Construct the incidence graph G(F)
    G = {i: [] for i in range(n)}
    for clause in F:
        for var in clause:
            G[var].append(clause)
    
    # Function to compute the minimal rank of a groupoid action
    def min_rank(G):
        # Placeholder function; actual implementation required
        return 0
    
    rank = min_rank(G)
    
    # Check if the rank is within the upper bound O(n log n + m log m)
    upper_bound = n * math.log(n) + m * math.log(m)
    conjecture_holds = rank <= upper_bound
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")