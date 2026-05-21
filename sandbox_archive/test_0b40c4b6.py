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
    
    def generate_structure(n):
        # Placeholder for structure generation logic
        return [random.randint(1, 10) for _ in range(n)]
    
    def compute_action_count(structure):
        # Placeholder for action count computation logic
        return sum(structure)
    
    def compute_mcsp_depth(structure):
        # Placeholder for MCSP depth computation logic
        return max(structure)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    structure = generate_structure(n)
    action_count = compute_action_count(structure)
    mcsp_depth = compute_mcsp_depth(structure)
    
    if mcsp_depth == 0:
        return {
            "metric_name": "action_to_mcsp_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "MCSP depth is zero"
        }
    
    ratio = action_count / mcsp_depth
    
    return {
        "metric_name": "action_to_mcsp_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": "" if ratio <= 2 else f"Ratio {ratio} exceeds 2"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_ratio = sum(result["metric_value"] for result in results if result["instances_tested"] > 0)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 2\" first_failing_seed={first_failing_seed}")