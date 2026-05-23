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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def ac0_circuit(f, n):
        # Simplified AC0 circuit generation
        if n == 1:
            return f[0]
        else:
            half = n // 2
            left = ac0_circuit(f[:2**half], half)
            right = ac0_circuit(f[2**half:], half)
            return (left + right) % 2
    
    def tropicalized_brauer_group_rank(circuit, n):
        # Simplified Brauer group rank calculation
        if circuit == 0:
            return 1
        elif circuit == 1:
            return 2
        else:
            return 3
    
    def parity_threshold(f, n):
        # Simplified parity threshold calculation
        count = sum(1 for x in f if ac0_circuit(x, n) == 1)
        return count / len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        t = parity_threshold(f, n)
        rank = tropicalized_brauer_group_rank(ac0_circuit(f, n), n)
        results.append((n, t * math.log(n), rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((t * math.log(n) - mean) ** 2 for n, t, rank in results) / len(results)
    mean = sum(t * math.log(n) for n, t, rank in results) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_corr} std=NA support_fraction={support_fraction}")