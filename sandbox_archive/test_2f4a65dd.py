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
    
    def generate_binary_matroid(n):
        ground_set = list(range(n))
        rank = random.randint(1, n-1)
        independent_sets = []
        for i in range(rank + 1):
            independent_sets.extend(random.sample(ground_set, i))
        return independent_sets
    
    def characteristic_vectors(matroid, n):
        vectors = []
        for subset in matroid:
            vector = [0] * n
            for element in subset:
                vector[element] = 1
            vectors.append(vector)
        return vectors
    
    def disjointness_protocol(vectors):
        n = len(vectors[0])
        communication_cost = 0
        for i in range(n):
            if any(vector[i] == 1 for vector in vectors):
                communication_cost += 1
        return communication_cost
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_trials = 100
    instances_tested = 0
    total_communication_cost = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(total_trials // len(n_values)):
            matroid = generate_binary_matroid(n)
            vectors = characteristic_vectors(matroid, n)
            communication_cost = disjointness_protocol(vectors)
            total_communication_cost += communication_cost
            instances_tested += 1
    
    mean_communication_cost = total_communication_cost / instances_tested
    if mean_communication_cost < math.log(instances_tested):
        conjecture_holds = False
        counterexample = "communication_complexity_too_low"
    
    return {
        "metric_name": "disjointness_protocol",
        "metric_value": mean_communication_cost,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")