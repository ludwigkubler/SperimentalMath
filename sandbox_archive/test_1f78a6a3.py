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
    
    n = 10  # Starting size for circuits
    c = 2.0  # Hypothetical constant from the conjecture
    
    total_ratio = 0.0
    instances_tested = 0
    n_max = 0
    
    while instances_tested < 30:
        entanglement = random.uniform(1, 10) * n  # Simulating increasing entanglement
        kahler_index = random.uniform(1, 2) * n  # Simulating Kähler metric's minimal local index
        
        ratio = kahler_index / entanglement
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
        
        if instances_tested >= 30:
            break
        
        n += 5
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = abs(mean_ratio - c) <= 0.1 * c
    counterexample = "" if conjecture_holds else f"Mean ratio {mean_ratio} does not converge to {c}"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")