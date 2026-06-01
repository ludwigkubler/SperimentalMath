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
    
    def communication_protocol(n):
        # Example protocol: a simple binary protocol with rank n
        return [random.randint(0, 1) for _ in range(n)]
    
    def communication_rank(protocol):
        # Example ranking: number of 1s in the protocol
        return sum(protocol)
    
    def quadratic_intersections(rank):
        # Example computation: quadratic intersections are proportional to rank^2
        return rank ** 2
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        protocol = communication_protocol(n)
        rank = communication_rank(protocol)
        mi = quadratic_intersections(rank)
        
        if mi > 1.2 * rank:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, MI={mi}"
            break
        
        instances_tested += 1
        total_metric_value += mi / math.log(n)
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    
    return {
        "metric_name": "minimal_quadratic_intersections",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if abs((r["metric_value"] - math.log(r["n_max"])) / math.log(r["n_max"]) - r["communication_rank"]) > 0.2 * r["communication_rank"]) >= len(results) * 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"MI ratio deviates by more than 20% from κ(P)\" first_failing_seed={seeds[results.index(next(r for r in results if abs((r['metric_value'] - math.log(r['n_max'])) / math.log(r['n_max']) - r['communication_rank']) > 0.2 * r['communication_rank']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")