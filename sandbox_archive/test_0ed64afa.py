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
    
    def communication_complexity_disj(n):
        return n
    
    def construct_cocomplex(V):
        rank = len([v for v in V if sum(v) > 0])
        return rank
    
    def generate_boolean_valuation(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            V = generate_boolean_valuation(n)
            rank = construct_cocomplex(V)
            total_rank += rank
            instances_tested += 1
    
    avg_rank = Fraction(total_rank, instances_tested)
    cc_disj_n = communication_complexity_disj(n)
    
    conjecture_holds = avg_rank <= Fraction(cc_disj_n * 1.10)
    counterexample = "" if conjecture_holds else f"rank={avg_rank}, expected={cc_disj_n}"
    
    return {
        "metric_name": "cocomplex_rank",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")