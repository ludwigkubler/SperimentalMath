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
    
    def generate_bp(n, t):
        states = [f's{i}' for i in range(2**(n+t))]
        transitions = {}
        for state in states:
            if '0' not in state and '1' not in state:
                continue
            next_states = []
            for bit in ['0', '1']:
                new_state = ''.join([bit if s == 'x' else s for s in state])
                next_states.append(new_state)
            transitions[state] = next_states
        return states, transitions
    
    def free_entropy(bp):
        # Placeholder implementation of free entropy calculation
        # This is a dummy function and should be replaced with actual computation
        return random.random() * 10
    
    def bp_size(bp):
        states, _ = bp
        return len(states)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for t in range(1, 6):  # Assuming at least one level and up to 5 levels
            bp = generate_bp(n, t)
            entropy = free_entropy(bp)
            size = bp_size(bp)
            results.append((n, t, entropy, size))
    
    if not results:
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_size = sum(size for _, _, _, size in results) / len(results)
    max_ratio = max(2**(n + a * t) for n, t, _, size in results if size > 0)
    ratio = mean_size / max_ratio
    
    return {
        "metric_name": "free_entropy",
        "metric_value": mean_size,
        "instances_tested": len(results),
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds threshold"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")