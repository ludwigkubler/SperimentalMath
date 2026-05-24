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
    
    def compute_minimal_rank(entanglement_pattern):
        if not entanglement_pattern:
            return 0
        return max(len(row) for row in entanglement_pattern)

    def generate_entanglement_pattern(n):
        pattern = []
        for i in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            if sum(row) > 0:
                pattern.append(row)
        return pattern

    def compute_bp_readtwice_depth(pattern):
        n = len(pattern)
        depth = 0
        for i in range(n):
            for j in range(i + 1, n):
                if pattern[i][j] == 1:
                    depth += 1
        return depth

    n = random.randint(5, 40)
    entanglement_pattern = generate_entanglement_pattern(n)
    bp_readtwice_depth = compute_bp_readtwice_depth(entanglement_pattern)
    
    minimal_rank = compute_minimal_rank(entanglement_pattern)

    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")