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
    
    def frege_proof_width(phi):
        # Placeholder implementation for Frege proof width calculation
        return len(phi.split())

    def find_algebraic_roots(phi):
        # Placeholder implementation for finding algebraic roots
        # This is a dummy function and should be replaced with actual logic
        return set([random.randint(1, 10) for _ in range(len(phi.split()))])

    phi = " ".join(random.choices("01", k=random.randint(5, 20)))
    w_phi = frege_proof_width(phi)
    R_phi = find_algebraic_roots(phi)
    
    return {
        "metric_name": "R(φ) - w(φ)",
        "metric_value": abs(len(R_phi) - w_phi),
        "instances_tested": 1,
        "n_max": len(phi.split()),
        "conjecture_holds": abs(len(R_phi) - w_phi) <= 3 * w_phi / 2,
        "counterexample": "" if conjecture_holds else f"phi={phi}, R(φ)={len(R_phi)}, w(φ)={w_phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")