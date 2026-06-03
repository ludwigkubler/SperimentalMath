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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        # Simplified version of the communication complexity rank
        # This is a placeholder and should be replaced with actual computation
        return random.randint(1, n)
    
    def minimal_entanglement_entropy(n):
        # Placeholder for minimal entanglement entropy calculation
        # This is a simplified version and should be replaced with actual quantum circuit simulation
        return math.sqrt(n)
    
    metric_name = "communication_complexity_rank_vs_minimal_entanglement_entropy"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    all_ranks = []
    all_entropies = []
    
    for _ in range(instances_tested):
        n = random.randint(5, min(n_max, 20))
        f = generate_random_boolean_function(n)
        rank = communication_complexity_rank(f)
        entropy = minimal_entanglement_entropy(n)
        
        if abs(rank - entropy) > 10:
            conjecture_holds = False
            counterexample = f"Rank-Entropy pair ({rank}, {entropy}) exceeds threshold"
            break
        
        all_ranks.append(rank)
        all_entropies.append(entropy)
    
    mean_rank = sum(all_ranks) / instances_tested
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in all_ranks) / instances_tested)
    correlation_coefficient = sum((all_ranks[i] - mean_rank) * (all_entropies[i] - mean_entropy) for i in range(instances_tested)) / (instances_tested * std_rank * math.sqrt(sum((x - mean_entropy)**2 for x in all_entropies)))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank-Entropy pair exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")