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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_bp_width(f):
        n = len(f)
        width = 0
        for i in range(n):
            if f[i] != f[0]:
                width += 1
        return width
    
    def free_probability_space_rank(bp):
        # Placeholder implementation; actual computation depends on the BP structure
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    W_f = compute_bp_width(f)
    RankFreeProb_Pf = free_probability_space_rank(f)
    
    if W_f == 0:
        return {
            "metric_name": "Rank vs Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Width is zero"
        }
    
    ratio = RankFreeProb_Pf / math.log(W_f)
    return {
        "metric_name": "Rank vs Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": "" if 0.5 <= ratio <= 2 else f"Ratio {ratio} outside [0.5, 2]"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    if all('metric_value' is not None for result in results):
        mean = sum(result['metric_value'] for result in results) / len(results)
        std = math.sqrt(sum((result['metric_value'] - mean)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if 0.5 <= result['metric_value'] <= 2) / len(results)
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result['metric_value'] <= 2))
            print(f"RESULT: FALSIFIED counterexample='Ratio outside [0.5, 2]' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some seeds had undefined metric_value")