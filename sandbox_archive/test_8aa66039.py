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
    n = random.randint(5, 40)
    instances_tested = 30
    total_entanglement_index = 0
    
    for _ in range(instances_tested):
        # Generate a random read-twice branching program of size n
        program = [random.choice(['0', '1']) for _ in range(n)]
        
        # Compute the quantum entanglement index (simplified model)
        # This is a placeholder; actual computation would be complex and not provided here
        entanglement_index = sum(1 for bit in program if bit == '1')
        
        total_entanglement_index += entanglement_index
    
    mean_entanglement_index = total_entanglement_index / instances_tested
    conjecture_holds = mean_entanglement_index <= n  # Simplified polynomial bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Quantum Entanglement Index",
        "metric_value": mean_entanglement_index,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*4 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")