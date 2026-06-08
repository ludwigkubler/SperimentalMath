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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_rank_variance(f):
        n = int(math.log2(len(f)))
        rank_variances = []
        for i in range(2**n):
            count_0 = f[i].count(0)
            count_1 = f[i].count(1)
            rank_variances.append(abs(count_0 - count_1))
        return sum(rank_variances) / len(rank_variances)
    
    def quasi_plurality_group(f):
        n = int(math.log2(len(f)))
        group = set()
        for i in range(2**n):
            if f[i].count(0) > f[i].count(1):
                group.add(i)
            elif f[i].count(0) < f[i].count(1):
                group.add(i ^ (2**(n-1)-1))
        return len(group)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        delta_f = communication_rank_variance(f)
        Q_f = quasi_plurality_group(f)
        if delta_f == 0:
            continue
        results.append(Q_f / (delta_f ** 2))
    
    if not results:
        return {
            "metric_name": "Q_f / δ(f)^2",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "Q_f / δ(f)^2",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": all(x <= 10 for x in results),
        "counterexample": "" if all(x <= 10 for x in results) else "Q_f / δ(f)^2 > 10"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is None for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r <= 10) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(max([r for r in results if r > 10]))]
            print(f"RESULT: FALSIFIED counterexample=\"Q_f / δ(f)^2 > 10\" first_failing_seed={first_failing_seed}")