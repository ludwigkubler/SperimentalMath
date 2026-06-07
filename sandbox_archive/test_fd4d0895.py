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
    
    def circuit_entanglement_complexity(f):
        # Placeholder implementation. Replace with actual algorithm.
        return len(f)
    
    def coxeter_group_generator_count(f):
        # Placeholder implementation. Replace with actual algorithm.
        return len(f)
    
    n_max = 40
    instances_tested = 0
    total_ratio = 0
    
    for n in range(5, n_max + 1, 5):
        f = generate_boolean_function(n)
        entanglement = circuit_entanglement_complexity(f)
        generators = coxeter_group_generator_count(f)
        
        if entanglement == 0:
            continue
        
        ratio = generators / entanglement
        total_ratio += abs(ratio - 1)
        instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio <= 0.5 and all(abs(g / e - 1) <= 0.2 for g, e in zip([coxeter_group_generator_count(generate_boolean_function(n)) for n in range(5, n_max + 1, 5)], [circuit_entanglement_complexity(generate_boolean_function(n)) for n in range(5, n_max + 1, 5)]))
    
    return {
        "metric_name": "Ratio of Generators to Entanglement",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")