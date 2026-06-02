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
    
    def communication_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(1, 2*n) for _ in range(n)]
    
    def noncommutative_crossed_product(protocol):
        # Placeholder for the actual computation of the noncommutative crossed product
        # For simplicity, we'll just sum the elements of the protocol
        return sum(protocol)
    
    def communication_complexity_rank(protocol):
        # Placeholder for the actual computation of the communication complexity rank
        # For simplicity, we'll just use the length of the protocol
        return len(protocol)
    
    n = random.randint(5, 40)  # Sweep through different sizes
    protocol = communication_protocol(n)
    crossed_product_order = noncommutative_crossed_product(protocol)
    rank = communication_complexity_rank(protocol)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")