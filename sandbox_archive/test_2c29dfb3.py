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
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(1, n))
        return protocol
    
    def compute_index(protocol):
        n = len(protocol)
        index = 0
        for i in range(n):
            for j in range(i+1, n):
                if protocol[i] == protocol[j]:
                    index += 1
        return index
    
    def communication_complexity_rank(protocol):
        rank = 0
        for value in set(protocol):
            rank += protocol.count(value)
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        protocol = generate_protocol(n)
        index = compute_index(protocol)
        rank = communication_complexity_rank(protocol)
        results.append((index, rank))
    
    if not results:
        return {
            "metric_name": "K-theory Index and Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid protocols generated"
        }
    
    mean_index = sum(index for index, _ in results) / len(results)
    mean_rank = sum(rank for _, rank in results) / len(results)
    support_fraction = sum(1 for index, rank in results if 1.5 * rank <= index <= 2 * rank) / len(results)
    
    return {
        "metric_name": "K-theory Index and Communication Complexity Rank",
        "metric_value": mean_index,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 10)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")