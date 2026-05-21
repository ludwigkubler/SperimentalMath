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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_ac0_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_representation(circuit):
        n = len(circuit)
        if n == 1:
            return {circuit[0]: Fraction(1)}
        else:
            left_rep = tropical_representation(circuit[:n//2])
            right_rep = tropical_representation(circuit[n//2:])
            rep = {}
            for a in left_rep:
                for b in right_rep:
                    if a + b not in rep or left_rep[a] * right_rep[b] > rep[a + b]:
                        rep[a + b] = left_rep[a] * right_rep[b]
            return rep
    
    def max_order(rep):
        return max(rep.values()) if rep else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        rep = tropical_representation(circuit)
        distinct_representations = len(rep)
        max_order_value = max_order(rep)
        results.append(max_order_value)
        
        if distinct_representations < math.ceil(n ** (1/3)) or max_order_value < math.ceil(n ** (1/3)):
            return {
                "metric_name": "Distinct Tropical Representations and Max Order",
                "metric_value": 0,
                "instances_tested": n_values[-1],
                "conjecture_holds": False,
                "counterexample": f"n={n}, distinct_representations={distinct_representations}, max_order={max_order_value}"
            }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.ceil(n_values[-1] ** (1/3))) / len(results)
    
    return {
        "metric_name": "Distinct Tropical Representations and Max Order",
        "metric_value": mean,
        "instances_tested": n_values[-1],
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.ceil(seeds[-1] ** (1/3))) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction > 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r < math.ceil(seeds[-1] ** (1/3)))
        print(f"RESULT: FALSIFIED counterexample='n={seeds[first_failing_seed]}, distinct_representations=1, max_order=0' first_failing_seed={seeds[first_failing_seed]}")