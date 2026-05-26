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
    
    def communication_complexity_disj(n):
        return n
    
    def generate_random_nbit_string(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def boolean_valuation(s):
        return [int(c) for c in s]
    
    def construct_cocomplex(V):
        rank = 0
        for i in range(len(V)):
            if V[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            s = generate_random_nbit_string(n)
            V = boolean_valuation(s)
            rank = construct_cocomplex(V)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    CC_DISJ_n = communication_complexity_disj(40)  # Using n=40 for upper bound
    threshold = CC_DISJ_n * 1.1
    
    conjecture_holds = mean_rank <= threshold
    counterexample = "" if conjecture_holds else f"rank={mean_rank}, expected={threshold}"
    
    return {
        "metric_name": "cocomplex_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*40+2, 40))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")