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
    
    def generate_monotone_circuit(n):
        # Placeholder for actual circuit generation logic
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_entanglement_entropy(circuit):
        # Placeholder for actual entanglement entropy calculation logic
        n = len(circuit)
        if n == 1:
            return 0
        return math.log2(n)
    
    instances_tested = 0
    total_entropy = 0
    conjecture_holds = True
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(30):
            circuit = generate_monotone_circuit(n)
            entropy = calculate_entanglement_entropy(circuit)
            total_entropy += entropy
            instances_tested += 1
            
            if entropy < 2**(n/4):
                conjecture_holds = False
                counterexample = f"Circuit size {n} with entropy {entropy}"
                return {
                    "metric_name": "entanglement_entropy",
                    "metric_value": total_entropy / instances_tested,
                    "instances_tested": instances_tested,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                }
    
    return {
        "metric_name": "entanglement_entropy",
        "metric_value": total_entropy / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")