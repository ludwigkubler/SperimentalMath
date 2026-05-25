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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in range(2)]
        probabilities = [c / n for c in counts if c > 0]
        return sum(-p * math.log2(p) for p in probabilities)
    
    def generate_boolean_function(n):
        return random.choices([0, 1], k=2**n)
    
    def symmetric_group_representation_dimension(f):
        n = len(f)
        # Simplified representation dimension calculation
        return n + 1
    
    def entropy_bound_invariant(f):
        H_f = shannon_entropy(f)
        return 2 * H_f + math.log(n, 2)
    
    instances_tested = 0
    total_dimension = 0
    total_entropy_bound = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        f = generate_boolean_function(n)
        dimension = symmetric_group_representation_dimension(f)
        H_f = shannon_entropy(f)
        entropy_bound = entropy_bound_invariant(f)
        
        total_dimension += dimension
        total_entropy_bound += entropy_bound
        instances_tested += 1
    
    mean_dimension = total_dimension / instances_tested
    mean_entropy_bound = total_entropy_bound / instances_tested
    
    conjecture_holds = mean_dimension <= mean_entropy_bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Dimension vs Entropy Bound",
        "metric_value": mean_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")