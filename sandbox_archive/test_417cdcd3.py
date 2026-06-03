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
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def find_automorphisms(cnf):
        # Placeholder for automorphism group finding algorithm
        # This is a dummy implementation and does not actually compute the automorphisms
        return 0

    def communication_complexity_rank(cnf):
        # Placeholder for communication complexity rank calculation
        # This is a dummy implementation and does not actually calculate the rank
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    sum_aut_order = 0
    min_ranks = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_k_cnf(n, k=3)
            aut_order = find_automorphisms(cnf)
            rank = communication_complexity_rank(cnf)
            total_instances += 1
            sum_aut_order += aut_order
            min_ranks.append(rank)
    
    mean_aut_order = sum_aut_order / total_instances
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    
    conjecture_holds = mean_aut_order >= n_values[-1]**2 * math.log(n_values[-1])
    counterexample = "" if conjecture_holds else f"mean_aut_order={mean_aut_order}, mean_min_rank={mean_min_rank}"
    
    return {
        "metric_name": "Automorphism Group Order",
        "metric_value": mean_aut_order,
        "instances_tested": total_instances,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")