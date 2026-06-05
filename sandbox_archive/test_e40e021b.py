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
    
    def generate_circuit(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(circuit):
        n = len(circuit[0])
        width = 0
        for clause in circuit:
            width = max(width, sum(abs(x) for x in clause))
        return width
    
    def minimal_order(circuit):
        # Placeholder implementation of Algorithm X
        # This is a dummy function and should be replaced with the actual algorithm
        n = len(circuit[0])
        return n  # Dummy value
    
    metric_name = "correlation_coefficient"
    instances_tested = 30
    n_max = 40
    conjecture_holds = False
    counterexample = ""
    
    correlation_values = []
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        m_C = monotone_width(circuit)
        SO_Sheaf_C = minimal_order(circuit)
        
        if m_C == 0:
            continue
        
        correlation_values.append(SO_Sheaf_C / m_C)
    
    if len(correlation_values) < instances_tested:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": len(correlation_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    mean = sum(correlation_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in correlation_values) / instances_tested)
    
    if mean >= 0.95:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results))} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_proven\" first_failing_seed={first_failing_seed}")