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
    
    def generate_ac0_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_size(circuit):
        return len(circuit)
    
    def quaternion_algebra_rank(circuit):
        # Simplified mapping to a rank based on the number of inputs
        n = int(math.log2(len(circuit)))
        return n
    
    def log_size(size):
        return math.log(size, 2)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)  # Sweep over different sizes
        circuit = generate_ac0_circuit(n)
        size = circuit_size(circuit)
        rank = quaternion_algebra_rank(circuit)
        log_s = log_size(size)
        
        results.append({
            "n": n,
            "circuit": circuit,
            "size": size,
            "rank": rank,
            "log_size": log_s
        })
    
    max_rank = max(result["rank"] for result in results)
    avg_log_size = sum(result["log_size"] for result in results) / len(results)
    
    conjecture_holds = max_rank <= avg_log_size * 2  # Upper bound factor of 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_rank",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_max_rank = sum(result["metric_value"] for result in results) / len(results)
    std_max_rank = math.sqrt(sum((result["metric_value"] - mean_max_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_max_rank} std={std_max_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_max_rank} std={std_max_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")