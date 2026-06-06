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
    
    def calculate_groupoid_size(f, n):
        m = 0
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    m += 1
        return m
    
    def calculate_communication_complexity_rank(f, n):
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[1 << i] != f[1 << j]:
                    rank += 1
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        m_n = calculate_groupoid_size(f, n)
        rank = calculate_communication_complexity_rank(f, n)
        results.append((m_n, rank))
    
    if not results:
        return {
            "metric_name": "Variance Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    m_ns, ranks = zip(*results)
    var_rank = variance(ranks)
    conjecture_holds = Fraction(m_ns[0], n_values[0]) <= var_rank <= Fraction(m_ns[-1], n_values[-1])
    counterexample = "" if conjecture_holds else f"Variance Ratio: {var_rank}, Expected Range: [{Fraction(m_ns[0], n_values[0]), Fraction(m_ns[-1], n_values[-1])}]"
    
    return {
        "metric_name": "Variance Ratio",
        "metric_value": var_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(results):
        return
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")