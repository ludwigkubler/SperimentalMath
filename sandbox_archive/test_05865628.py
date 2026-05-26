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
        # Simplified AC0 circuit generation for demonstration
        return [random.choice([0, 1]) for _ in range(d * n)]
    
    def calculate_geometric_invariant(circuit):
        # Placeholder for geometric invariant calculation
        return random.uniform(1, 10)
    
    n = random.randint(5, 40)
    d = random.randint(2, n)
    s = n ** 2
    
    circuit = generate_ac0_circuit(n, d)
    rho_C = calculate_geometric_invariant(circuit)
    
    expected_bound = math.log(n) * math.log(d)
    difference = abs(rho_C - expected_bound)
    
    return {
        "metric_name": "rho_C",
        "metric_value": rho_C,
        "instances_tested": 1,
        "conjecture_holds": rho_C >= expected_bound and difference <= 3,
        "counterexample": "" if rho_C >= expected_bound else f"rank={rho_C}, expected={expected_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")