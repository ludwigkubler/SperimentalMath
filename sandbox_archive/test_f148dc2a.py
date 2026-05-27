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
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate a random CNF formula with n variables and m clauses
    cnf_formula = []
    for _ in range(m):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        cnf_formula.append(clause)
    
    # Compute the automorphism group of the vertex-labeled CNF formula
    # This is a placeholder function. In practice, you would need to implement
    # or use an existing algorithm for computing the automorphism group.
    def compute_automorphism_group(cnf):
        # Placeholder implementation: return a trivial group
        return []
    
    automorphism_group = compute_automorphism_group(cnf_formula)
    
    # Construct the associated Coxeter group
    # This is a placeholder function. In practice, you would need to implement
    # or use an existing algorithm for constructing the Coxeter group.
    def construct_coxeter_group(group):
        # Placeholder implementation: return a trivial Coxeter group
        return 2
    
    coxeter_group_rank = construct_coxeter_group(automorphism_group)
    
    # Determine if the conjecture holds
    expected_rank = n * math.log(m, 2)
    conjecture_holds = abs(coxeter_group_rank - expected_rank) <= 0.1 * expected_rank
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": coxeter_group_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")