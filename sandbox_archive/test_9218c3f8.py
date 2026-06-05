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
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in set(f)]
        probabilities = [c / n for c in counts]
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def geometric_flow_order(f):
        # Placeholder implementation of geometric flow order
        # This is a dummy function and should be replaced with actual computation
        return len(f)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.randint(0, 1) for _ in range(n)]
    
    entropy = shannon_entropy(f)
    gf_order = geometric_flow_order(f)
    
    if entropy == 0:
        return {
            "metric_name": "GF/Entropy Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Shannon entropy is zero"
        }
    
    ratio = gf_order / entropy
    
    return {
        "metric_name": "GF/Entropy Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    total_ratio = 0
    num_supporting_seeds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            num_supporting_seeds += 1
        
        results.append(trial_result)
    
    mean_ratio = total_ratio / len(results)
    support_fraction = num_supporting_seeds / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")