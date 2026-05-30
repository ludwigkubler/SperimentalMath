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
    
    def generate_boolean_function(N):
        return [random.choice([0, 1]) for _ in range(2**N)]
    
    def circuit_depth(f):
        N = int(math.log2(len(f)))
        if N == 0:
            return 0
        depth = 1
        while len(f) > 1:
            f = [f[i] ^ f[i + 1] for i in range(0, len(f), 2)]
            depth += 1
        return depth
    
    def generality_of_functor(f):
        N = int(math.log2(len(f)))
        if N == 0:
            return 1
        return N + 1
    
    n_max = 40
    instances_tested = 0
    total_depth = 0
    total_generality = 0
    
    for _ in range(30):
        N = random.randint(5, n_max)
        f = generate_boolean_function(N)
        depth = circuit_depth(f)
        generality = generality_of_functor(f)
        
        instances_tested += 1
        total_depth += depth
        total_generality += generality
    
    if instances_tested < 30:
        return {
            "metric_name": "circuit_depth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_depth = total_depth / instances_tested
    mean_generality = total_generality / instances_tested
    
    if mean_depth <= 10 * mean_generality:
        return {
            "metric_name": "circuit_depth",
            "metric_value": mean_depth,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "circuit_depth",
            "metric_value": mean_depth,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_depth={mean_depth} > 10 * mean_generality={10 * mean_generality}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 40))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("counterexample" in result and result["counterexample"] != "" for result in results):
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=NA support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")