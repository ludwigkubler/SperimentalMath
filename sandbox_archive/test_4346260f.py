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
        # Placeholder function to simulate communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def minimal_entanglement_entropy(n):
        # Placeholder function to simulate minimal entanglement entropy
        # This is a dummy implementation and should be replaced with actual logic
        return math.sqrt(n)
    
    instances_tested = 0
    all_ranks = []
    all_entropies = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        rank = communication_complex_rank(f)
        entropy = minimal_entanglement_entropy(n)
        
        if rank is not None and entropy is not None:
            all_ranks.append(rank)
            all_entropies.append(entropy)
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid samples generated"
        }
    
    mean_rank = sum(all_ranks) / instances_tested
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in all_ranks) / instances_tested)
    mean_entropy = sum(all_entropies) / instances_tested
    std_entropy = math.sqrt(sum((x - mean_entropy)**2 for x in all_entropies) / instances_tested)
    
    correlation_coefficient = sum((all_ranks[i] - mean_rank) * (all_entropies[i] - mean_entropy) for i in range(instances_tested)) / (instances_tested * std_rank * math.sqrt(sum((x - mean_entropy)**2 for x in all_entropies)))
    
    conjecture_holds = abs(correlation_coefficient) >= 0.5 and max(abs(all_ranks[i] - all_entropies[i]) for i in range(instances_tested)) <= 10
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank-Entropy pair with difference > 10: {max(abs(all_ranks[i] - all_entropies[i]) for i in range(instances_tested))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'] != 'mapping_undefined')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")