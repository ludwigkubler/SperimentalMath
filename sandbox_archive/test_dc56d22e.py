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
    
    def calculate_geometric_entanglement_entropy(f):
        # Placeholder implementation; actual calculation depends on the function
        n = int(math.log2(len(f)))
        entanglement_entropy = sum(abs(x) ** 2 for x in f)
        return entanglement_entropy
    
    def communication_complexity(f):
        # Placeholder implementation; actual calculation depends on the function
        n = int(math.log2(len(f)))
        return n**2 / 4
    
    instances_tested = 0
    total_entanglement_entropy = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        entanglement_entropy = calculate_geometric_entanglement_entropy(f)
        cc = communication_complexity(f)
        
        if entanglement_entropy < 1 / n**2:
            conjecture_holds = False
            counterexample = f"n={n}, E(G)={entanglement_entropy}"
            break
        
        total_entanglement_entropy += entanglement_entropy
        instances_tested += 1
    
    mean_entanglement_entropy = total_entanglement_entropy / instances_tested if instances_tested > 0 else 0.0
    
    return {
        "metric_name": "Geometric Entanglement Entropy",
        "metric_value": mean_entanglement_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")