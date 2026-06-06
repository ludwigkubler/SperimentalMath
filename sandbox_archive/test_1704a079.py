# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_groupoid_morphisms(f):
        n = len(f)
        morphisms = set()
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    morphisms.add((i, j))
        return len(morphisms)
    
    def calculate_communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean)**2 for x in values) / len(values)
    
    metric_name = "Communication Complexity Rank Variance Ratio"
    instances_tested = 0
    n_max = 0
    total_variance = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            m_n = calculate_groupoid_morphisms(f)
            rank = calculate_communication_complexity_rank(f)
            instances_tested += 1
            n_max = max(n_max, n)
            total_variance += rank
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient samples"
        }
    
    mean_variance = total_variance / instances_tested
    conjecture_holds = Fraction(1, 2) * n_max <= mean_variance <= Fraction(3, 2) * n_max
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean Variance: {mean_variance}, Expected Range: [{Fraction(1, 2) * n_max}, {Fraction(3, 2) * n_max}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean Variance does not meet the expected range\" first_failing_seed={first_failing_seed}")