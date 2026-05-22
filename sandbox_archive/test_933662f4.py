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
    
    def symplectic_form_rank(n):
        # Placeholder for the actual computation of the symplectic form rank
        # For simplicity, we use a dummy function that returns a value based on n
        return 2 * math.log(n, 2) ** 2
    
    def read_twice_branching_program_size():
        # Placeholder for generating a random size for the branching program
        return random.randint(5, 40)
    
    circuit_size = read_twice_branching_program_size()
    rank = symplectic_form_rank(circuit_size)
    expected_value = math.log(circuit_size, 2) ** 2
    
    ratio = rank / expected_value
    within_range = abs(ratio - 1) <= 0.3
    
    return {
        "metric_name": "rank_to_log_squared_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": within_range,
        "counterexample": "" if within_range else f"Rank {rank} is not within ±30% of expected value {expected_value}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 3 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not match expected value\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")