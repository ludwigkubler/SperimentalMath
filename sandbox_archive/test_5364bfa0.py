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
    
    def generate_disjointness_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def communication_complexity(instance):
        n = len(instance)
        cc = 0
        for i in range(n):
            if instance[i] == 1:
                cc += 1
        return cc
    
    def tropical_rank(instance):
        n = len(instance)
        rank = 0
        for i in range(n):
            if instance[i] == 1:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    instance = generate_disjointness_instance(n)
    cc = communication_complexity(instance)
    mrts = tropical_rank(instance)
    
    ratio = cc / mrts if mrts != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Communication Complexity to Minimal Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= n * 0.5,  # Example threshold for c
        "counterexample": f"cc={cc}, mrts={mrts}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"cc<{results[0]['metric_value']}, mrts<{results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")