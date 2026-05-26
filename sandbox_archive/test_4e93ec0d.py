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
    
    def generate_disjointness_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_free_probability_entanglement_rank(disjointness_function):
        n = int(math.log2(len(disjointness_function)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if disjointness_function[i] != disjointness_function[j]:
                    rank += 1
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst):
        m = mean(lst)
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(5):
            disjointness_function = generate_disjointness_function(n)
            rank = compute_free_probability_entanglement_rank(disjointness_function)
            ranks.append(rank)
    
    mean_value = mean(ranks)
    std_value = std(ranks)
    conjecture_holds = all(rank > n**2 * math.log(n) + 3 * std_value for rank in ranks)
    counterexample = "" if conjecture_holds else "rank= {}, expected= {}".format(mean_value, n_values[0]**2 * math.log(n_values[0]))
    
    return {
        "metric_name": "free_probability_entanglement_rank",
        "metric_value": mean_value,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")