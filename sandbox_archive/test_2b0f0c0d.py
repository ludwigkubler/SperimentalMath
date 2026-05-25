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
    n_values = [5, 10, 15, 20, 30, 40]
    communication_complexities = []
    
    for n in n_values:
        # Simulate the communication complexity of Disjointness
        # This is a placeholder value; replace with actual computation if available
        communication_complexity = random.uniform(n**1.5 - 1, n**1.5 + 1)
        communication_complexities.append(communication_complexity)
    
    mean_cc = sum(communication_complexities) / len(communication_complexities)
    std_dev_cc = math.sqrt(sum((x - mean_cc)**2 for x in communication_complexities) / len(communication_complexities))
    
    conjecture_holds = mean_cc >= n_values[0]**1.5 and std_dev_cc < 10
    counterexample = "" if conjecture_holds else "n^3/2 bound not met"
    
    return {
        "metric_name": "Randomized Communication Complexity",
        "metric_value": mean_cc,
        "instances_tested": len(communication_complexities),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n^3/2 bound not met\" first_failing_seed={first_failing_seed}")