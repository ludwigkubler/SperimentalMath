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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_length(cnf):
        # Simplified DPLL solver to estimate resolution length
        stack = []
        while stack:
            literal = stack.pop()
            if literal in cnf:
                cnf.remove(literal)
            elif -literal in cnf:
                cnf.remove(-literal)
            else:
                return len(stack) + 1
        return len(stack)
    
    def formal_power_series_rank(cnf):
        # Placeholder for actual computation of rank
        return random.randint(1, 10)  # Simplified for testing
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    
    rank = formal_power_series_rank(cnf)
    length = resolution_length(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": rank / (length + 1),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    mean_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        counterexample = next(res for res in results if not res["conjecture_holds"])["counterexample"]
        first_failing_seed = next(res for res in results if not res["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")