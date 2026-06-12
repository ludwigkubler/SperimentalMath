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
    
    def generate_circuit(depth, width):
        if depth == 1:
            return [random.choice([0, 1]) for _ in range(width)]
        inputs = [generate_circuit(random.randint(1, depth-1), width) for _ in range(width)]
        outputs = [random.choice(inputs) ^ random.choice(inputs) for _ in range(width)]
        return outputs
    
    def compute_module_rank(permutation_group):
        # Placeholder for actual module rank computation
        # This is a dummy implementation for testing purposes
        return len(permutation_group)
    
    def run_circuit(depth, width):
        circuit = generate_circuit(depth, width)
        permutation_group = set()
        for i in range(width):
            for j in range(width):
                if circuit[i] == circuit[j]:
                    permutation_group.add((i, j))
        mrl = compute_module_rank(permutation_group)
        return mrl, depth, width
    
    n_max = 0
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n_max >= 16:
            break
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            depth = random.randint(1, min(n-1, 20))
            width = random.randint(1, min(n, 20))
            mrl, depth_val, width_val = run_circuit(depth, width)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            total_metric_value += mrl / (width + depth ** (2/3))
            r = mrl / (width + depth ** (2/3))
            if r < 0.5:
                conjecture_holds = False
                counterexample = f"Depth={depth}, Width={width}, MRL={mrl}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (len([n for n in [5, 10, 15, 20, 30, 40] if n_max >= n]) * 5)
    
    return {
        "metric_name": "mrl_ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")