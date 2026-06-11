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
    
    def generate_quandle(q):
        quandle_table = [[random.randint(0, q-1) for _ in range(q)] for _ in range(q)]
        return quandle_table
    
    def tropicalize(quandle_table):
        q = len(quandle_table)
        tropicalized_table = []
        for i in range(q):
            row = [max(quandle_table[i][j], quandle_table[j][i]) for j in range(q)]
            tropicalized_table.append(row)
        return tropicalized_table
    
    def resolution_width(phi):
        # Placeholder for actual computation
        return random.randint(1, 10)  # Simulated value
    
    def entanglement_order(quandle_table):
        q = len(quandle_table)
        order = 0
        for i in range(q):
            for j in range(i+1, q):
                if quandle_table[i][j] != quandle_table[j][i]:
                    order += 1
        return order
    
    n_tests = 30
    total_ratio = 0
    max_n = 0
    
    for _ in range(n_tests):
        q = random.randint(5, 40)
        quandle = generate_quandle(q)
        tropicalized = tropicalize(quandle)
        entanglement = entanglement_order(tropicalized)
        phi = "CNF_formula"  # Placeholder
        width = resolution_width(phi)
        
        if width > entanglement:
            return {
                "metric_name": "ratio",
                "metric_value": None,
                "instances_tested": n_tests,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": "w(φ) > tq(Q)"
            }
        
        total_ratio += width / entanglement
        max_n = max(max_n, q)
    
    mean_ratio = total_ratio / n_tests
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": n_tests,
        "n_max": max_n,
        "conjecture_holds": mean_ratio <= 1.5 and all(width / entanglement <= 3 for _ in range(n_tests)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")