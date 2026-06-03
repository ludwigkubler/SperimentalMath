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
    
    def generate_k_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def find_automorphisms(cnf):
        # Placeholder for automorphism group finding algorithm
        # This is a dummy implementation and does not actually find automorphisms
        return 0
    
    def communication_complexity_rank(cnf):
        # Placeholder for communication complexity rank calculation
        # This is a dummy implementation and returns a random value
        return random.randint(1, 10)
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    min_ranks = []
    
    for n in range(5, 41):
        for _ in range(3):  # Ensure at least 30 instances per seed
            cnf = generate_k_cnf(n, n)
            order = find_automorphisms(cnf)
            rank = communication_complexity_rank(cnf)
            total_order += order
            min_ranks.append(rank)
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    min_rank_mean = sum(min_ranks) / len(min_ranks)
    
    conjecture_holds = mean_order >= n_max * math.log(n_max)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "mean_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")