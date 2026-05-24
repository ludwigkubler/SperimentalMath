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
    
    def generate_function_field(g):
        # Simplified function field generation for demonstration
        return [random.randint(1, g**2) for _ in range(g)]
    
    def find_min_order(G, k):
        # Simplified minimal order finding for demonstration
        for x in G:
            if all(x**i % len(G) != 1 for i in range(1, len(G))):
                return x
    
    def quantum_query_complexity(A, k):
        # Simplified quantum query complexity for demonstration
        return len(A)**2
    
    g = random.randint(5, 40)
    K = generate_function_field(g)
    A = [random.choice(K) for _ in range(g)]
    
    min_order = find_min_order(A, g)
    Q_BELL_k = quantum_query_complexity(A, g)
    
    alpha = Fraction(1, 2)  # Simplified constant for demonstration
    lower_bound = alpha * g**2
    upper_bound = O(alpha * g**2)
    
    conjecture_holds = min_order >= lower_bound and Q_BELL_k <= upper_bound
    
    return {
        "metric_name": "quantum_query_complexity",
        "metric_value": Q_BELL_k,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"min_order={min_order}, lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")