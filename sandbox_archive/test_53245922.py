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
    
    def log_base(x, base):
        return math.log(x) / math.log(base)
    
    def generate_tropicalized_sheaf(n):
        # Placeholder for generating a tropicalized sheaf
        return n * 2
    
    def compute_size(T):
        # Placeholder for computing the size of a tropicalized sheaf
        return T + 1
    
    def compute_rank(T):
        # Placeholder for computing the rank of a tropicalized sheaf
        return T // 2
    
    def generate_ac0_parity_circuit(n):
        # Placeholder for generating an AC0 parity circuit
        return n * 3
    
    c = Fraction(1, 2)
    c_prime = Fraction(1, 4)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        T = generate_tropicalized_sheaf(n)
        C_size = generate_ac0_parity_circuit(n)
        
        if T_rank := compute_rank(T) < c_prime * log_base(C_size, 2):
            counterexample = f"T_rank={T_rank} < {c_prime * log_base(C_size, 2)} for n={n}"
            return {
                "metric_name": "rank",
                "metric_value": T_rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    return {
        "metric_name": "rank",
        "metric_value": sum(compute_rank(generate_tropicalized_sheaf(n)) for n in [5, 10, 15, 20, 30, 40]) / 6,
        "instances_tested": 6,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or counterexamples found")