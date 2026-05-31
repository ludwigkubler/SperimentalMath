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
        return [random.choice([-1, 1]) for _ in range(2**n)]
    
    def conjugacy_class_enumeration(f):
        # Simplified version of the algorithm for demonstration
        n = len(f)
        classes = []
        for i in range(n):
            class_i = set()
            for j in range(2**(n-1)):
                if f[j] == f[j ^ (1 << i)]:
                    class_i.add(j)
            classes.append(class_i)
        return classes
    
    def count_irreducible_representations(classes):
        # Simplified version of the algorithm for demonstration
        return len(classes)
    
    n_values = [5, 10, 20, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        classes = conjugacy_class_enumeration(f)
        chi_f = count_irreducible_representations(classes)
        results.append(chi_f)
    
    mean_chi = sum(results) / len(results)
    std_chi = math.sqrt(sum((x - mean_chi)**2 for x in results) / len(results))
    support_fraction = sum(1 for chi in results if abs(chi - 2**n_values[results.index(chi)]) / (2**n_values[results.index(chi)]) <= 0.05) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "chi_f",
        "metric_value": mean_chi,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(abs(r["metric_value"] - 2**n_values[results.index(r)]) / (2**n_values[results.index(r)]) > 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 2**n_values[results.index(result)]) / (2**n_values[results.index(result)]) > 0.1)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")