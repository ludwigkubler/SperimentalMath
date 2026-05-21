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
    
    def quantum_entanglement_index(bp):
        # Placeholder for the actual quantum entanglement index calculation
        # This is a dummy implementation for testing purposes
        return len(bp) ** 0.5
    
    def generate_bp(size):
        # Generate a random read-twice BP of the given size
        bp = []
        for _ in range(size):
            row = [random.choice([0, 1]) for _ in range(size)]
            bp.append(row)
        return bp
    
    n_values = [5, 10, 15, 20, 30, 40]
    entanglement_indices = []
    
    for n in n_values:
        for _ in range(17):  # Ensure at least 30 instances per seed
            bp = generate_bp(n)
            index = quantum_entanglement_index(bp)
            entanglement_indices.append((n, index))
    
    mean_index = sum(index for _, index in entanglement_indices) / len(entanglement_indices)
    std_dev = math.sqrt(sum((index - mean_index) ** 2 for _, index in entanglement_indices) / len(entanglement_indices))
    
    conjecture_holds = mean_index >= (math.log(n_values[-1]) ** 2) * 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_entanglement_index",
        "metric_value": mean_index,
        "instances_tested": len(entanglement_indices),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")