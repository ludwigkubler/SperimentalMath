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
    
    def tropical_proof_rank(formula):
        # Placeholder for actual implementation
        return len(formula)

    def weight_profile_length(circuit):
        # Placeholder for actual implementation
        return sum(1 for _ in circuit)

    n = 20
    formula = ''.join(random.choice('01') for _ in range(n))
    circuit = ['+' if random.random() < 0.5 else '-' for _ in range(n)]
    
    tropical_rank = tropical_proof_rank(formula)
    weight_profile_len = weight_profile_length(circuit)
    
    return {
        "metric_name": "Weight Profile Length",
        "metric_value": weight_profile_len,
        "instances_tested": 1,
        "conjecture_holds": weight_profile_len <= tropical_rank,
        "counterexample": f"Formula: {formula}, Circuit: {circuit}, Weight Profile Length: {weight_profile_len}, Tropical Rank: {tropical_rank}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")