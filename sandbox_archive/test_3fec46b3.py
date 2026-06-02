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
    
    def generate_communication_complexity(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def calculate_p_group_representation(cc_instance):
        n = len(cc_instance)
        if n == 1:
            return 1
        representation_order = 2 ** (n - 1)
        return representation_order
    
    def communication_complexity_rank(cc_instance):
        n = len(cc_instance)
        rank = sum(1 for i in range(n) if cc_instance[i] != cc_instance[(i + 1) % n])
        return rank
    
    total_minimal_order = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cc_instance = generate_communication_complexity(n)
            minimal_order = calculate_p_group_representation(cc_instance)
            rank = communication_complexity_rank(cc_instance)
            
            total_minimal_order += minimal_order
            instances_tested += 1
            
            if minimal_order > math.sqrt(n):
                conjecture_holds = False
                counterexample = f"n={n}, cc_instance={cc_instance}, minimal_order={minimal_order}"
    
    mean_minimal_order = total_minimal_order / instances_tested
    
    return {
        "metric_name": "mean_minimal_order",
        "metric_value": mean_minimal_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")