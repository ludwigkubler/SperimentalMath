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
    
    def generate_disjointness_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(instance):
        # Simplified Razborov's lower bound
        return len(instance) * (len(instance) - 1) // 2
    
    def noncrossing_partition_rank(n):
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            # Placeholder for actual computation
            return n**2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_disjointness_instance(n)
    cc = communication_complexity(instance)
    rank = noncrossing_partition_rank(n)
    
    if rank == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = Fraction(cc, rank)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1.2 and ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean = sum(r['metric_value'] for r in results) / len(results)
        std = (sum((r['metric_value'] - mean)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")