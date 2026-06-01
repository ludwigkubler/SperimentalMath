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
    
    def communication_complexity(f):
        # Placeholder function to compute communication complexity
        return len(f)

    def minimal_order(abelian_system):
        # Placeholder function to compute minimal order of abelian integral system
        return len(abelian_system)

    def generate_boolean_function(n):
        # Generate a random Boolean function with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = n
        conjecture_holds = True
        counterexample = ""

        for _ in range(5):  # Test each size with 5 random functions
            f = generate_boolean_function(n)
            c_f = communication_complexity(f)
            abelian_system_f = [i for i, val in enumerate(f) if val == 1]  # Placeholder abelian system
            order_f = minimal_order(abelian_system_f)

            instances_tested += 1

            if c_f > Fraction(2 * n, 3):
                if order_f < Fraction(n, 3):
                    conjecture_holds = False
                    counterexample = f"n={n}, c(f)={c_f}, order_f={order_f}"
                    break

        results.append({
            "metric_name": "communication_complexity",
            "metric_value": c_f,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })

    return {
        "seed": seed,
        **results[0],
        "mean_metric_value": sum(res["metric_value"] for res in results) / len(results),
        "std_metric_value": (sum((res["metric_value"] - results[0]["mean_metric_value"])**2 for res in results) / len(results))**0.5,
        "support_fraction": sum(1 for res in results if res["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            break

    if len(results) == len(seeds):
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={results[0]['mean_metric_value']:.2f} std={results[0]['std_metric_value']:.2f} support_fraction={support_fraction:.2f}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=early_refutation n_tested={len(results)}")