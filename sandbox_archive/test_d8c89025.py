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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        # Placeholder function; replace with actual implementation
        return len(f)
    
    def min_order(monomial_ideal):
        # Placeholder function; replace with actual implementation
        return len(monomial_ideal)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    comm_rank_f = communication_complexity_rank(f)
    min_order_I_f = min_order(f)
    
    if min_order_I_f <= (2 * n) / 3:
        expected_comm_rank = 2
    else:
        expected_comm_rank = None
    
    diff = abs(comm_rank_f - expected_comm_rank) if expected_comm_rank is not None else float('inf')
    
    return {
        "metric_name": "communication_complexity_rank_diff",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": diff <= 3,
        "counterexample": "" if diff <= 3 else f"comm_rank({f}) = {comm_rank_f}, min_order(I_{f}) = {min_order_I_f}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")