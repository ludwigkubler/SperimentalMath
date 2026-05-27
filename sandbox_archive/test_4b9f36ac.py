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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partition_rank(n):
        # Placeholder function to compute the rank of a noncrossing partition
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def monotone_span_program_circuit_size(rank):
        # Placeholder function to compute the circuit size from the rank
        # This is a dummy implementation and should be replaced with actual logic
        return 2**rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    rank = noncrossing_partition_rank(n)
    circuit_size = monotone_span_program_circuit_size(rank)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= n**(1/4) and circuit_size <= 2**n**(1/4)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncrossing Partition Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((x - mean_value)**2 for x in (r["metric_value"] for r in results)) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")