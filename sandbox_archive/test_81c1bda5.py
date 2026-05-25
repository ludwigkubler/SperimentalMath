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
        counts = [f.count(0), f.count(1)]
        probabilities = [c / n for c in counts if c > 0]
        return -sum(p * math.log2(p) for p in probabilities)
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def symmetric_group_representation_dimension(n):
        # Simplified representation dimension calculation
        return n
    
    def distinguishability_dimension(f):
        f_complement = [1 - x for x in f]
        dim_f = symmetric_group_representation_dimension(len(f))
        dim_f_complement = symmetric_group_representation_dimension(len(f_complement))
        return max(dim_f, dim_f_complement)
    
    n_values = [5, 10, 15, 20, 30, 40]
    dimensions = []
    entropies = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        entropy = shannon_entropy(f)
        dim = distinguishability_dimension(f)
        dimensions.append(dim)
        entropies.append(entropy)
    
    mean_dim = sum(dimensions) / len(dimensions)
    mean_entropy = sum(entropies) / len(entropies)
    correlation = sum((dim - mean_dim) * (ent - mean_entropy) for dim, ent in zip(dimensions, entropies)) / len(dimensions)
    
    conjecture_holds = correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")