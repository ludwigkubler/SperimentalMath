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

K_2 = Fraction(1, 2).sqrt()

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = f.index(1)
    return n + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    K_2_n_minus_1 = K_2 ** (39)
    metric_value = 0
    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41):
        if n > n_max:
            n_max = n

        for _ in range(30 // (n - 4)):
            f = generate_boolean_function(n)
            cc = communication_complexity(f)
            instances_tested += 1
            ratio = Fraction(cc, K_2_n_minus_1)

            if abs(ratio - 1) > Fraction(5, 100):
                conjecture_holds = False
                counterexample = f"n={n}, cc={cc}, ratio={ratio}"
                break

        if not conjecture_holds:
            break

    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")