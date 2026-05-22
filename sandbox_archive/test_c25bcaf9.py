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
    
    def generate_disjointness_instance(n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        return inputs
    
    def calculate_entanglement_dimension(instance):
        n = len(instance)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            # Simplified example: entanglement dimension is n
            return n
    
    instances_tested = 0
    min_entanglement_dimension = float('inf')
    
    for _ in range(30):
        instance = generate_disjointness_instance(random.randint(5, 40))
        entanglement_dimension = calculate_entanglement_dimension(instance)
        if entanglement_dimension < min_entanglement_dimension:
            min_entanglement_dimension = entanglement_dimension
        instances_tested += 1
    
    conjecture_holds = min_entanglement_dimension >= random.randint(5, 40) / 2
    counterexample = "" if conjecture_holds else f"n={min_entanglement_dimension}, entanglement_dimension={min_entanglement_dimension}"
    
    return {
        "metric_name": "Minimal Entanglement Dimension",
        "metric_value": min_entanglement_dimension,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")