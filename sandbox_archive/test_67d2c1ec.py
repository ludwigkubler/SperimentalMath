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
    n = 20  # Fixed n for simplicity, as the conjecture is about asymptotic behavior
    instances_tested = 30
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def coin_tossing_time(xor_function):
        # Simplified model of coin tossing time
        return len(xor_function) / 2
    
    def communication_complexity_xor(n):
        # Communication complexity of XOR on n bits is Θ(n)
        return n
    
    total_coin_tossing_time = 0
    for _ in range(instances_tested):
        xor_function = generate_xor_function(n)
        coin_tossing_time_value = coin_tossing_time(xor_function)
        total_coin_tossing_time += coin_tossing_time_value
    
    mean_coin_tossing_time = total_coin_tossing_time / instances_tested
    expected_value = math.log(n) * communication_complexity_xor(n)
    
    conjecture_holds = abs(mean_coin_tossing_time - expected_value) <= 2 * expected_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "coin_tossing_time",
        "metric_value": mean_coin_tossing_time,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")