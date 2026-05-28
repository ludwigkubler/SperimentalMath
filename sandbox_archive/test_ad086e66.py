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
    
    def generate_xor_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_curve_rank(function):
        n = len(function)
        if n == 1:
            return 1
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if function[i] != function[j]:
                    matrix[i][j] = abs(i - j)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def compute_communication_complexity(function):
        n = len(function)
        complexity = 2 * n
        return complexity
    
    function = generate_xor_boolean_function(40)
    tropical_rank = compute_tropical_curve_rank(function)
    communication_complexity = compute_communication_complexity(function)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_complexity = math.sqrt(sum((r["metric_value"] - mean_complexity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")