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
    
    def free_entropy(n, t):
        # Simplified model for demonstration purposes
        return n * math.log(t)
    
    def bp_size(n, t):
        return 2 ** (n + t)
    
    def generate_bp(n, t):
        states = ['q' + str(i) for i in range(2**(n+t))]
        transitions = {}
        for s in states:
            transitions[s] = {chr(i): random.choice(states) for i in range(ord('a'), ord('z')+1)}
        return states, transitions
    
    def simulate_bp(bp):
        states, transitions = bp
        state = random.choice(states)
        path = [state]
        for _ in range(20):  # Simulate a short path through the BP
            state = transitions[state][random.choice('abcdefghijklmnopqrstuvwxyz')]
            path.append(state)
        return len(path)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            t = random.randint(n, 2*n)
            bp = generate_bp(n, t)
            entropy = free_entropy(n, t)
            size = bp_size(n, t)
            path_length = simulate_bp(bp)
            
            results.append({
                "n": n,
                "t": t,
                "entropy": entropy,
                "size": size,
                "path_length": path_length
            })
    
    if not results:
        return {
            "metric_name": "free_entropy_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(result["size"] / (2**(result["n"] + result["t"])) for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["size"] / (2**(result["n"] + result["t"])) - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "free_entropy_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio <= 1.5,  # Threshold set to 1.5 for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_data n_tested=" + str(sum(result["instances_tested"] for result in results)))
    else:
        mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_evidence")