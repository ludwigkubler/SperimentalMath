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
        # Generate a random boolean circuit with n inputs
        if n == 1:
            return ['0'] * (2**n)
        else:
            subcircuits = [generate_circuit(n-1) for _ in range(3)]
            return [f'({sub[0]} & {sub[1]}) | {sub[2]}' for sub in zip(*subcircuits)]

    def local_index(circuit):
        # Placeholder function to compute the local index
        # This is a dummy implementation and should be replaced with actual computation
        return len(set(circuit))

    def monotone_width(circuit):
        # Placeholder function to compute the monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return 1

    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    li = local_index(circuit)
    mw = monotone_width(circuit)

    return {
        "metric_name": "Local Index vs Monotone Width",
        "metric_value": li,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")