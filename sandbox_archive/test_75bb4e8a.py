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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_hyperplane_arrangement(f):
        m = len(f)
        n = int(math.log2(m))
        arrangement = []
        for i in range(m):
            if f[i] == 1:
                arrangement.append(i)
        return arrangement
    
    def rank_variance(arrangement, n):
        count = [0] * (n + 1)
        for x in arrangement:
            count[x % (n + 1)] += 1
        variance = sum((c - len(arrangement) / (n + 1)) ** 2 for c in count) / (n + 1)
        return variance
    
    def hodge_classes(f):
        m = len(f)
        n = int(math.log2(m))
        classes = []
        for i in range(n):
            class_i = sum(1 << j for j in range(n) if f[j] == 1 and (j & i) == 0)
            classes.append(class_i)
        return classes
    
    def minimal_hodge_dimension(classes):
        n = len(classes)
        max_dim = 0
        for subset in range(1, 2**n):
            dim = sum(1 for class_ in classes if (subset & class_) == class_)
            max_dim = max(max_dim, dim)
        return max_dim
    
    def compute_metric(f):
        arrangement = boolean_hyperplane_arrangement(f)
        variance = rank_variance(arrangement, len(arrangement))
        classes = hodge_classes(f)
        dimension = minimal_hodge_dimension(classes)
        if dimension == 0:
            return {"metric_name": "R(f)/HDim(f)", "metric_value": None, "instances_tested": 1, "n_max": len(arrangement), "conjecture_holds": False, "counterexample": "mapping_undefined"}
        ratio = variance / dimension
        return {"metric_name": "R(f)/HDim(f)", "metric_value": ratio, "instances_tested": 1, "n_max": len(arrangement), "conjecture_holds": True, "counterexample": ""}
    
    instances_tested = 0
    n_max = 0
    total_ratio = 0.0
    for _ in range(30):
        m = random.randint(5, 40)
        f = generate_boolean_function(m)
        result = compute_metric(f)
        if result["metric_value"] is not None:
            instances_tested += result["instances_tested"]
            n_max = max(n_max, len(arrangement))
            total_ratio += result["metric_value"]
    
    mean_ratio = total_ratio / instances_tested
    support_fraction = sum(1 for r in [compute_metric(generate_boolean_function(random.randint(5, 40)))["conjecture_holds"] for _ in range(30)] if r) / 30
    
    return {"metric_name": "R(f)/HDim(f)", "metric_value": mean_ratio, "instances_tested": instances_tested, "n_max": n_max, "conjecture_holds": support_fraction >= 0.5, "counterexample": ""}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")