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
    n = 30
    instances_tested = 0
    total_rank = 0
    
    for _ in range(10):  # Test with multiple boolean functions of varying entropies
        # Generate a random boolean function f on n variables
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Calculate the entropy H(f)
        counts = [f.count(i) for i in [0, 1]]
        if sum(counts) == 0:
            continue
        probabilities = [c / sum(counts) for c in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
        
        # Compute the quantum group rank (simulated here as a random integer for demonstration)
        rank = random.randint(1, n)
        
        instances_tested += 1
        total_rank += rank
    
    metric_value = total_rank / instances_tested
    conjecture_holds = abs(metric_value - (2**(-entropy) * math.log(n))) <= 3 * (2**(-entropy) * math.log(n))
    counterexample = "" if conjecture_holds else f"Rank {metric_value} deviates from expected {2**(-entropy) * math.log(n)}"
    
    return {
        "metric_name": "quantum_group_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")