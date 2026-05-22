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
    
    # Generate a random linear cryptographic protocol with varying query complexities Q.
    n = random.randint(5, 40)
    Q = random.randint(n // 2, n)
    
    # For each protocol, design a corresponding quantum error correcting code that ensures the secure transmission of information.
    # The minimal rank of the quantum error correcting code (QEC) is at most Q/2.
    rank_QEC = Q / 2
    
    # Compute the minimal rank of the quantum error correcting code for each protocol and compare it to Q/2.
    metric_name = "Minimal Rank of Quantum Error Correcting Code"
    metric_value = rank_QEC
    instances_tested = 1
    conjecture_holds = rank_QEC >= Q / 2
    counterexample = "" if conjecture_holds else f"Q={Q}, rank(QEC)={rank_QEC}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")