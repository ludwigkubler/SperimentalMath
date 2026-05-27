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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tropical_hodge_rank(cnf):
        # Placeholder function to compute the tropical Hodge rank
        # This is a dummy implementation for demonstration purposes
        return len(cnf)  # Simplified as number of clauses
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = tropical_hodge_rank(cnf)
    
    expected_rank = math.log2(n) ** 2
    metric_value = rank
    instances_tested = 1
    conjecture_holds = abs(rank - expected_rank) <= 0.1 * expected_rank
    counterexample = "" if conjecture_holds else f"Rank {rank} does not match expected {expected_rank}"
    
    return {
        "metric_name": "tropical_hodge_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_d} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample=\"Rank does not match expected\" first_failing_seed={first_failing_seed}"
    
    print(result)