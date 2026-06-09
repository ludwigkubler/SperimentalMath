# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n literals
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def formal_group_representation(circuit):
        # Compute the minimal order of a formal group representation
        # This is a placeholder function; replace it with actual computation
        return len(circuit)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        circuit = generate_circuit(n)
        order = formal_group_representation(circuit)
        results.append({"n": n, "order": order})
    
    if not results:
        return {
            "metric_name": "c",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["order"] / r["n"] ** Fraction(1, 2) for r in results]
    mean_value = sum(metric_values) / len(metric_values)
    max_n = max(r["n"] for r in results)
    
    return {
        "metric_name": "c",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": all(v <= 1.5 for v in metric_values),
        "counterexample": "" if all(v <= 1.5 for v in metric_values) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=conjecture_holds_false")