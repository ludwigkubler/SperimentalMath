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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def tropical_diameter(f):
    n = int(math.log2(len(f)))
    points = []
    for i in range(2**n):
        point = []
        for j in range(n):
            if (i >> j) & 1:
                point.append(1)
            else:
                point.append(-math.inf)
        points.append(point)
    
    max_distance = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = sum(max(p1, p2) - min(p1, p2) for p1, p2 in zip(points[i], points[j]))
            if distance > max_distance:
                max_distance = distance
    return max_distance

def ac0_parity_circuit_size(f):
    n = int(math.log2(len(f)))
    size = 0
    for i in range(n):
        count = sum(1 for x in f if (x >> i) & 1)
        if count % 2 == 1:
            size += 1
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        trop_diameter = tropical_diameter(f)
        circuit_size = ac0_parity_circuit_size(f)
        
        if circuit_size > O(trop_diameter * math.log(n)):
            return {
                "metric_name": "AC0 Parity Circuit Size",
                "metric_value": circuit_size,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, trop_diameter={trop_diameter}, circuit_size={circuit_size}"
            }
    
    return {
        "metric_name": "AC0 Parity Circuit Size",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

def O(x):
    return x

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= O(trop_diameter(f) * math.log(n)) for n, f in zip([5, 10, 15, 20, 30, 40], [generate_random_boolean_function(n) for _ in range(len(results))])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > O(trop_diameter(f) * math.log(n)) for n, f in zip([5, 10, 15, 20, 30, 40], [generate_random_boolean_function(n) for _ in range(len(results))])):
        print(f"RESULT: FALSIFIED counterexample='n={n}, trop_diameter={trop_diameter(f)}, circuit_size={ac0_parity_circuit_size(f)}' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")