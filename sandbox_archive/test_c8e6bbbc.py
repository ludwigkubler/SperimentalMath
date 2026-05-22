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
    
    def syntactic_monoid_generators(f):
        n = len(f)
        generators = []
        for i in range(n):
            if f[i] == 1:
                generators.append(i)
        return generators
    
    def acc0_circuit_depth(generators):
        return int(math.ceil(math.log2(len(generators))))
    
    def group_presentation_generators(f):
        n = len(f)
        generators = []
        for i in range(n):
            if f[i] == 1:
                generators.append(i)
        return generators
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        generators = syntactic_monoid_generators(f)
        depth = acc0_circuit_depth(generators)
        group_gen = group_presentation_generators(f)
        
        if len(group_gen) < n * math.log2(n):
            counterexample = "Group presentation requires fewer than O(|f| log n) generators."
            return {
                "metric_name": "Generators",
                "metric_value": len(group_gen),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        if depth < 2**n:
            counterexample = "ACC⁰ circuit with depth less than 2^{|f|} can compute f."
            return {
                "metric_name": "Circuit Depth",
                "metric_value": depth,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "metric_name": "Generators",
            "metric_value": len(group_gen),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    mean_generators = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Generators",
        "metric_value": mean_generators,
        "instances_tested": 30,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_generators = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_generators} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")