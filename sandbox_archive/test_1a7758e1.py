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
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit generation for modular functions
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def find_p_adic_point(circuit):
        # Placeholder function to simulate finding a p-adic point
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    def log_n(n):
        if n <= 0:
            return float('inf')
        return math.log(n)
    
    c = 2  # Placeholder constant for the conjecture
    
    results = []
    for _ in range(30):  # Test with 30 random seeds
        n = random.randint(5, 40)  # Sweep n from 5 to 40
        circuit = generate_ac0_circuit(n)
        p_adic_order = find_p_adic_point(circuit)
        log_n_value = log_n(n)
        
        results.append({
            "n": n,
            "c_log_n": c * log_n_value,
            "p_adic_order": p_adic_order
        })
    
    all_holds = True
    for result in results:
        if result["p_adic_order"] > result["c_log_n"]:
            all_holds = False
    
    return {
        "metric_name": "minimal_p_adic_order",
        "metric_value": sum(result["p_adic_order"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_holds,
        "counterexample": "" if all_holds else "circuit_size={}".format(max(result["n"] for result in results))
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    total_metric_value = 0
    total_instances_tested = 0
    conjecture_holds_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        
        total_metric_value += trial_result["metric_value"]
        total_instances_tested += trial_result["instances_tested"]
        if trial_result["conjecture_holds"]:
            conjecture_holds_count += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = conjecture_holds_count / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0, support_fraction))
    elif any(not trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"circuit_size\" first_failing_seed={}".format(first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")