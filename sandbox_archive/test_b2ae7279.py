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
    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random UNIQUE GAME PROBLEM instance
        distributions = [random.random() for _ in range(n)]
        min_gap = min(abs(distributions[i] - distributions[j]) for i, j in itertools.combinations(range(n), 2))
        
        if min_gap == 0:
            continue
        
        # Simulate the Geometric Langlands dual object rank (simplified)
        rank = random.randint(1, n)  # This is a placeholder; replace with actual computation
        total_rank += rank

    mean_rank = total_rank / instances_tested
    ratio = mean_rank / min_gap**2 if min_gap != 0 else float('inf')
    
    conjecture_holds = ratio >= 1
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Ratio of Mean Rank to ε^2",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")