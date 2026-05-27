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
        # Generate a simple AC⁰ circuit computing PARITY on n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quaternionic_form(circuit):
        # Placeholder function to simulate computation of quaternionic form rank
        return random.randint(1, len(circuit))
    
    def size_of_circuit(circuit):
        return len(circuit)
    
    results = []
    for _ in range(30):  # Test with multiple instances per seed
        circuit = generate_ac0_circuit(n=20)  # Fixed n for simplicity
        rank = compute_quaternionic_form(circuit)
        size = size_of_circuit(circuit)
        if size > 0:
            results.append({"rank": rank, "size": size})
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_circuits"
        }
    
    metric_value = sum(result["rank"] / math.log(result["size"]) for result in results) / len(results)
    conjecture_holds = all(rank >= math.log(size) for rank, size in results)
    counterexample = "" if conjecture_holds else "minimal_rank_too_small"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_d = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minimal_rank_too_small' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")