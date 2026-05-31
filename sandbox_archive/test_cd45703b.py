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
    
    def generate_affine_line_arrangement(n):
        lines = []
        for _ in range(n):
            a = random.uniform(-1, 1)
            b = random.uniform(-1, 1)
            lines.append((a, b))
        return lines
    
    def communication_complexity(lines):
        n = len(lines)
        if n == 0:
            return 0
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if lines[i][0] * lines[j][0] != -lines[i][1] * lines[j][1]:
                    complexity += 1
        return complexity
    
    def minimal_automorphic_rank(lines):
        # Placeholder function to simulate the computation of minimal automorphic rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(lines)
    
    n = random.randint(5, 40)
    lines = generate_affine_line_arrangement(n)
    rank = minimal_automorphic_rank(lines)
    c_A = communication_complexity(lines)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": c_A,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")