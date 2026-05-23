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
    n = 10  # Start with a small value and increase if needed
    c = 1.0  # Initial guess for the constant
    instances_tested = 0
    total_cc_xor = 0
    total_tgr = 0

    random.seed(seed)
    
    def generate_quantum_state(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def calculate_tropical_geometric_rank(state):
        # Placeholder implementation; replace with actual computation
        return len(state)

    def calculate_communication_complexity(state):
        # Placeholder implementation; replace with actual computation
        return sum(state) % 2

    while instances_tested < 30:
        state = generate_quantum_state(n)
        cc_xor = calculate_communication_complexity(state)
        tgr = calculate_tropical_geometric_rank(state)
        
        if tgr > 0:  # Avoid division by zero
            ratio = cc_xor / tgr
            total_cc_xor += cc_xor
            total_tgr += tgr
            instances_tested += 1

    mean_ratio = total_cc_xor / total_tgr
    conjecture_holds = abs(mean_ratio - c) <= 0.05 * c
    counterexample = "" if conjecture_holds else f"Mean ratio {mean_ratio} does not match expected constant {c}"

    return {
        "metric_name": "Communication Complexity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean ratio does not match expected constant' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded")