# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def decision_tree_complexity(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid boolean function length")
        if n == 1:
            return 1
        mid = 2**(n-1)
        left = f[:mid]
        right = f[mid:]
        return 1 + max(decision_tree_complexity(left), decision_tree_complexity(right))
    
    def symplectic_reduction(n):
        # Simplified version of symplectic reduction for demonstration purposes
        return n
    
    def geometric_entropy(n):
        return -n * math.log2(1/n)
    
    communication_ranks = []
    entropies = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        rank = decision_tree_complexity(f)
        entropy = geometric_entropy(symplectic_reduction(n))
        communication_ranks.append(rank)
        entropies.append(entropy)
    
    correlation_coefficient = sum((r - mean_ranks) * (e - mean_entropies) for r, e in zip(communication_ranks, entropies)) / \
                               math.sqrt(sum((r - mean_ranks)**2 for r in communication_ranks) * sum((e - mean_entropies)**2 for e in entropies))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(communication_ranks),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": 0.5 < correlation_coefficient <= 0.7,
        "counterexample": "" if 0.5 < correlation_coefficient <= 0.7 else f"Correlation coefficient {correlation_coefficient} is out of the expected range [0.5, 0.7]"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(seeds)}")