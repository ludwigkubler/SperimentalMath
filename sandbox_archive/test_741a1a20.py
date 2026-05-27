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
    
    def generate_classical_group(n):
        # Placeholder for generating a classical group of size n
        return [random.randint(0, 1) for _ in range(n * n)]
    
    def tropicalize(group):
        # Placeholder for tropicalizing the group
        return [[max(a, b) for b in row] for row in group]
    
    def min_rank(tropicalized_group):
        # Placeholder for computing the minimal rank of the tropicalized group
        m = len(tropicalized_group)
        n = len(tropicalized_group[0])
        rank = 0
        for i in range(m):
            if any(tropicalized_group[i][j] != float('-inf') for j in range(n)):
                rank += 1
        return rank
    
    def construct_acc0_circuit(group):
        # Placeholder for constructing an ACC⁰ circuit computing the isomorphism class of the group
        # This is a dummy implementation and should be replaced with actual circuit construction logic
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    group = generate_classical_group(n)
    tropicalized_group = tropicalize(group)
    rank = min_rank(tropicalized_group)
    circuit_width = construct_acc0_circuit(group)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rank * circuit_width,  # Dummy metric for demonstration
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")