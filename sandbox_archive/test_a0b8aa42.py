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
    
    def generate_group(n):
        if n == 1:
            return {0}
        elif n == 2:
            return {0, 1}
        else:
            g = set()
            for i in range(1, n):
                g.add(i)
            return g
    
    def adjoint_representation(group, n):
        rep = [[0] * len(group) for _ in range(len(group))]
        for i, x in enumerate(group):
            for j, y in enumerate(group):
                if (x + y) % n in group:
                    rep[i][j] = 1
        return rep
    
    def communication_complexity_rank(rep):
        rank = 0
        for row in rep:
            if sum(row) > 0:
                rank += 1
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        group = generate_group(n)
        adj_rep = adjoint_representation(group, n)
        rank = communication_complexity_rank(adj_rep)
        results.append(rank)
    
    mean_variance = variance(results)
    min_order = len(group)
    
    return {
        "metric_name": "min_order_to_variance_ratio",
        "metric_value": min_order / mean_variance,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": False if min_order / mean_variance < 0.4 or min_order / mean_variance > 1.2 else True,
        "counterexample": "" if min_order / mean_variance >= 0.4 and min_order / mean_variance <= 1.2 else f"Ratio out of bounds: {min_order / mean_variance}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.8 <= r <= 1.2) / len(results)
    
    if all(0.8 <= r <= 1.2 for r in results):
        result = "SUPPORTED"
    elif any(r < 0.4 or r > 1.2 for r in results):
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.2f}")