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
    
    def fast_walsh_hadamard_transform(x):
        n = len(x)
        if n == 1:
            return x
        even = fast_walsh_hadamard_transform(x[0::2])
        odd = fast_walsh_hadamard_transform(x[1::2])
        result = [0] * n
        for i in range(n // 2):
            result[i] = even[i] + odd[i]
            result[i + n // 2] = even[i] - odd[i]
        return result
    
    def additive_energy(coeffs):
        n = len(coeffs)
        energy = 0
        for i in range(n):
            for j in range(i, n):
                if coeffs[i] * coeffs[j] != 0:
                    energy += 1
        return energy
    
    n = random.randint(5, 40)
    sipser_function = [random.choice([0, 1]) for _ in range(2**n)]
    
    fourier_coeffs = fast_walsh_hadamard_transform(sipser_function)
    energy = additive_energy(fourier_coeffs)
    
    metric_value = energy
    instances_tested = 1
    conjecture_holds = energy >= 2**(n/2)
    counterexample = "" if conjecture_holds else f"mean_energy={energy} < 2^{n/2}"
    
    return {
        "metric_name": "additive_energy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_energy<{2**(n/2)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")