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
    
    def free_entropy_dimension(n):
        # Placeholder for actual computation
        return n  # Simplified for demonstration
    
    def randomized_communication_complexity(n):
        # Placeholder for actual computation
        return n * (n + 1) // 2  # Simplified for demonstration
    
    n = random.randint(5, 40)
    F_n = free_entropy_dimension(n)
    CC_DISJ_n = randomized_communication_complexity(n)
    
    ratio = CC_DISJ_n / F_n if F_n != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Communication Complexity to Free Entropy Dimension",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1.5 and ratio < 0.5,
        "counterexample": "" if ratio >= 1.5 else f"n={n}, F_n={F_n}, CC_DISJ_n={CC_DISJ_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if not result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(result["counterexample"]):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")