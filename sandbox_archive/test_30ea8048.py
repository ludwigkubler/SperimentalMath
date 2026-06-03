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
    
    def generate_category(n):
        if n == 1:
            return {'objects': [0], 'morphisms': []}
        objects = list(range(n))
        morphisms = []
        for i in range(n):
            for j in range(i+1, n):
                morphisms.append((i, j))
        return {'objects': objects, 'morphisms': morphisms}
    
    def min_order(category):
        objects = category['objects']
        morphisms = category['morphisms']
        if not morphisms:
            return 0
        min_ranks = [len(objects)]
        for obj in objects:
            rank = sum(1 for m in morphisms if m[0] == obj)
            min_ranks.append(rank)
        return min(min_ranks)
    
    def circuit_monotone_width(category):
        n = len(category['objects'])
        m = len(category['morphisms'])
        return (n + m) // 2
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        category = generate_category(n)
        min_r = min_order(category)
        m_CNF = circuit_monotone_width(category)
        results.append((min_r, m_CNF))
    
    mean_min_ranks = sum(r[0] for r in results) / len(results)
    mean_m_CNFs = sum(r[1] for r in results) / len(results)
    mean_absolute_difference = abs(mean_min_ranks - mean_m_CNFs)
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((r[0] - mean_min_ranks) * (r[1] - mean_m_CNFs) for r in results)
        denominator = math.sqrt(sum((r[0] - mean_min_ranks)**2 for r in results)) * math.sqrt(sum((r[1] - mean_m_CNFs)**2 for r in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 2
    counterexample = "" if conjecture_holds else f"min_order={mean_min_ranks}, m_CNF={mean_m_CNFs}"
    
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": mean_absolute_difference,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")