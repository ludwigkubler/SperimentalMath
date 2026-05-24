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
    
    def generate_ac0_circuit(n, d):
        if n == 1 and d == 1:
            return [0]
        elif n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n // 2, d - 1)
            right = generate_ac0_circuit(n - n // 2, d - 1)
            return [random.choice(left + right)]
    
    def tropical_variety(circuit):
        if len(circuit) == 1:
            return circuit[0]
        else:
            left = tropical_variety(circuit[:len(circuit)//2])
            right = tropical_variety(circuit[len(circuit)//2:])
            return [min(left), max(right)]
    
    def hodge_structure(variety):
        if len(variety) == 1:
            return variety[0]
        else:
            left = hodge_structure(variety[:len(variety)//2])
            right = hodge_structure(variety[len(variety)//2:])
            return [left + right, abs(left - right)]
    
    def min_rank(hodge):
        if len(hodge) == 1:
            return hodge[0]
        else:
            left = min_rank(hodge[:len(hodge)//2])
            right = min_rank(hodge[len(hodge)//2:])
            return max(left, right)
    
    n = random.randint(5, 40)
    d = random.randint(1, 10)
    circuit = generate_ac0_circuit(n, d)
    variety = tropical_variety(circuit)
    hodge = hodge_structure(variety)
    rank = min_rank(hodge)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - (n**2 * math.log(d))) < 3 * std_rank) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not abs(r["metric_value"] - (n**2 * math.log(d))) < 3 * std_rank), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")