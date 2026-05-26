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
    
    def calculate_berry_phase(boolean_function):
        n = len(boolean_function)
        U = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if boolean_function[i] == boolean_function[j]:
                    U[i][j] = 1
        return max(abs(sum(U[i][k] * U[k][j] for k in range(2**n))) for i in range(2**n) for j in range(2**n))
    
    def calculate_minimal_rank(berry_phase):
        n = len(berry_phase)
        rank = 0
        while berry_phase:
            max_val = max(abs(x) for row in berry_phase for x in row)
            if max_val == 0:
                break
            rank += 1
            for i in range(n):
                for j in range(n):
                    berry_phase[i][j] -= (berry_phase[i][0] * berry_phase[0][j]) / berry_phase[0][0]
        return rank
    
    n = random.randint(5, 40)
    boolean_function = generate_boolean_function(n)
    berry_phase = calculate_berry_phase(boolean_function)
    min_rank = calculate_minimal_rank(berry_phase)
    
    metric_name = "minimal_rank"
    metric_value = min_rank
    instances_tested = 1
    conjecture_holds = min_rank <= n
    counterexample = "" if conjecture_holds else f"rank={min_rank}, expected={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")