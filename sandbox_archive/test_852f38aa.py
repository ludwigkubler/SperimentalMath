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
    
    def generate_monoidal_category(n):
        if n == 1:
            return [[0]], [0], {0: 0}
        objects = list(range(n))
        morphisms = {}
        for i in range(n):
            morphisms[i] = []
            for j in range(n):
                if i != j:
                    morphisms[i].append(j)
        return morphisms, objects, morphisms
    
    def calculate_local_indeterminacy(morphisms, objects):
        n = len(objects)
        local_indet = 0
        for obj in objects:
            local_indet += len(morphisms[obj])
        return local_indet / n
    
    def calculate_communication_complexity_rank(morphisms, objects):
        n = len(objects)
        rank = 0
        for i in range(n):
            rank += max(len(morphisms[obj]) for obj in objects if obj != i)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    local_indet_sum = 0
    comm_complexity_rank_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        morphisms, objects, morphisms_dict = generate_monoidal_category(n)
        local_indet = calculate_local_indeterminacy(morphisms, objects)
        comm_complexity_rank = calculate_communication_complexity_rank(morphisms, objects)
        
        local_indet_sum += local_indet
        comm_complexity_rank_sum += comm_complexity_rank
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_local_indet = local_indet_sum / instances_tested
    mean_comm_complexity_rank = comm_complexity_rank_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(local_indet * rank for local_indet, rank in zip(local_indets, comm_complexity_ranks)) -
                                mean_local_indet * mean_comm_complexity_rank) / \
                               math.sqrt((instances_tested * sum(local_indet**2 for local_indet in local_indets) - mean_local_indet**2) *
                                         (instances_tested * sum(rank**2 for rank in comm_complexity_ranks) - mean_comm_complexity_rank**2))
    
    conjecture_holds = abs(correlation_coefficient) > 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")