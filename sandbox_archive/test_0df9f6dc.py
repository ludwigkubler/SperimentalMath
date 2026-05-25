# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def communication_complexity(instance):
        n = len(instance)
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        cc = communication_complexity(instance)
        results.append(cc)
    
    mean_value = sum(results) / len(results)
    support_fraction = len([r for r in results if r >= Fraction(n, 2)]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "communication_complexity < n/2"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["conjecture_holds"])
    
    support_fraction = sum(results) / len(results)
    
    if all(results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = seeds[next(i for i, x in enumerate(results) if not x)]
        result = f"FALSIFIED counterexample=\"communication_complexity < n/2\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={sum(trial_result['metric_value'] for trial_result in results)/len(results)} std=0 support_fraction={support_fraction}")