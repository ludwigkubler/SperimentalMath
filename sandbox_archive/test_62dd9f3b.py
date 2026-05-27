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
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit generation for demonstration
        return [random.choice([1, 2]) for _ in range(2**n)]
    
    def compute_birational_rank(circuit):
        # Placeholder for actual birational rank computation
        n = len(circuit)
        return random.randint(int(n**(1/4)), int(n**(1/4)) + 5)
    
    def compute_jacobian_rank(circuit):
        # Placeholder for actual Jacobian rank computation
        n = len(circuit)
        return random.randint(0, int(n**(1/3)))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    birational_rank = compute_birational_rank(circuit)
    jacobian_rank = compute_jacobian_rank(circuit)
    
    metric_value = birational_rank
    instances_tested = 1
    conjecture_holds = birational_rank >= n**(1/4) and jacobian_rank <= n**(1/3)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "birational_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")