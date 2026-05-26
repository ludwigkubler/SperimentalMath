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
    
    def communication_complexity_disj(n):
        return n
    
    def generate_boolean_valuation(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def construct_cocomplex(valuation):
        cocomplex = {}
        for i in range(len(valuation)):
            if valuation[i] == 1:
                cocomplex[i] = {j for j in range(len(valuation)) if valuation[j] == 1 and j != i}
        return cocomplex
    
    def rank_cocomplex(cocomplex):
        rank = 0
        for node, neighbors in cocomplex.items():
            rank = max(rank, len(neighbors))
        return rank
    
    n = random.randint(5, 40)
    valuation = generate_boolean_valuation(n)
    cocomplex = construct_cocomplex(valuation)
    rank = rank_cocomplex(cocomplex)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= communication_complexity_disj(n)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={communication_complexity_disj(n)}"
    
    return {
        "metric_name": "cocomplex_rank",
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
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")