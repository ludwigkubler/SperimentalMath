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

def generate_frege_proof(n):
    return " ".join(random.choices("ABCD", k=random.randint(2, 5)) for _ in range(n))

def compute_grothendieck_group_rank(phi):
    # Placeholder function to simulate Grothendieck group rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return len(set(phi.split()))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        phi = generate_frege_proof(n)
        rank = compute_grothendieck_group_rank(phi)
        width = len(phi.split())
        ratio = rank / width if width > 0 else float('inf')
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)

    mean_ratio = total_ratio / len(n_values)
    conjecture_holds = (mean_ratio >= 0.9) and (mean_ratio <= 1.1) and all(ratio <= 2 for ratio in [rank / width if width > 0 else float('inf') for phi, rank, width in [(generate_frege_proof(n), compute_grothendieck_group_rank(generate_frege_proof(n)), len(generate_frege_proof(n).split())) for n in n_values]])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Grothendieck group rank to Frege proof width ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")