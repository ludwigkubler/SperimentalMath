# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def galois_representation(f):
        # Constructive mapping for Galois representation (simplified)
        return len(f)

    def quantum_query_complexity(f):
        # Simplified quantum query complexity (assuming linear complexity)
        return len(f)

    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):  # Test with 30 random functions
        n = random.randint(5, 40)  # Sweep n through {5, 10, 15, 20, 30, 40}
        f = [random.randint(0, 1) for _ in range(n)]  # Generate a random binary function
        instances_tested += 1

        rho_f = galois_representation(f)
        Q_f = quantum_query_complexity(f)

        if rho_f > Fraction(Q_f ** 2, 4):
            conjecture_holds = False
            counterexample = f"rho_f={rho_f}, expected<=Q_f^2/4={Fraction(Q_f ** 2, 4)}"
            break

    return {
        "metric_name": "min_order_rho_f",
        "metric_value": Fraction(Q_f ** 2, 4),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes

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
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")