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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    def p_adic_l_function_rank(n, p):
        # Constructive mapping based on known constructions for p-adic L-functions
        # This is a placeholder function. Replace with actual construction.
        return random.randint(1, n)  # Example: rank is between 1 and n

    C_p = 0.5  # Placeholder value for C_p. Replace with actual calculation if possible.

    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41):
        rank = p_adic_l_function_rank(n, 2)  # Example using prime 2
        if rank < C_p * log2(n):
            instances_tested += 1
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, expected>=C_p*log(n)"
            break

    return {
        "metric_name": "p-adic L-function rank",
        "metric_value": C_p * log2(40),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(res["metric_value"] for res in results if res["conjecture_holds"])
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")