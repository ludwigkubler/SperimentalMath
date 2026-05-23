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
    
    def generate_qma_instance(n):
        clauses = []
        for _ in range(n):
            clause_size = random.randint(1, n)
            clause = [random.randint(1, 2*n) for _ in range(clause_size)]
            clauses.append(clause)
        return clauses
    
    def compute_configuration_space(clauses):
        # Placeholder for actual configuration space computation
        # For simplicity, we'll use a dummy rank based on the number of clauses
        return len(clauses)
    
    def bp_read_twice_circuit_threshold(n):
        # Placeholder for actual BP_ReadTwice circuit threshold computation
        # For simplicity, we'll use a dummy value based on n
        return 2 ** (n // 2)
    
    n = random.randint(5, 40)
    clauses = generate_qma_instance(n)
    rank = compute_configuration_space(clauses)
    bp_threshold = bp_read_twice_circuit_threshold(n)
    
    if rank < 2 ** (n // 2):
        return {
            "metric_name": "Rank vs BP_ReadTwice",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Configuration space rank below θ(n)"
        }
    
    correlation_coefficient = rank / bp_threshold
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        mean_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        if any(result["metric_value"] < 0.8 for result in results):
            result_type = "FALSIFIED"
            counterexample = "Correlation coefficient less than 0.8"
        else:
            result_type = "INCONCLUSIVE"
            counterexample = ""
    
    print(f"RESULT: {result_type} mean={mean_value} std=NA support_fraction={support_fraction}")