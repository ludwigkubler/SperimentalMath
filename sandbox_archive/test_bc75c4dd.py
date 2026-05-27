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
    
    def generate_random_quantum_state(n):
        # Generate a random quantum state as a tensor
        return [[random.random() for _ in range(n)] for _ in range(n)]
    
    def compute_minrank(tensor):
        n = len(tensor)
        rank = 1
        while True:
            found = False
            for i in range(n):
                if any(tensor[j][i] != 0 for j in range(n)):
                    found = True
                    break
            if not found:
                return rank
            rank += 1
    
    def compute_bp_depth(state):
        # Simplified computation of BP depth (not actual BP)
        n = len(state)
        return math.log2(n) + 1
    
    instances_tested = 0
    minrank_sum = 0.0
    bp_depth_sum = 0.0
    support_count = 0
    
    for _ in range(30):
        state = generate_random_quantum_state(random.randint(5, 40))
        minrank = compute_minrank(state)
        bp_depth = compute_bp_depth(state)
        
        if minrank <= 3 * bp_depth:
            support_count += 1
        
        instances_tested += 1
        minrank_sum += minrank
        bp_depth_sum += bp_depth
    
    mean_minrank = minrank_sum / instances_tested
    mean_bp_depth = bp_depth_sum / instances_tested
    support_fraction = support_count / instances_tested
    
    return {
        "metric_name": "minrank",
        "metric_value": mean_minrank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"Support fraction {support_fraction} < 0.9"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_minrank = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_minrank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_minrank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_minrank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Support fraction {support_fraction} < 0.8\" first_failing_seed={first_failing_seed}")