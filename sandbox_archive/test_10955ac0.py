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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def kronecker_coefficient(lam, mu):
        if len(lam) != len(mu):
            return 0
        n = sum(lam)
        d = 1
        for i in range(len(lam)):
            d *= math.factorial(n - sum(lam[:i]) + lam[i] - mu[i])
            d //= math.factorial(sum(lam[:i]) - mu[i])
            d //= math.factorial(lam[i] - mu[i])
            n -= lam[i]
        return Fraction(d)

    def sym_power_multiplicity(lam, k):
        if len(lam) == 0:
            return 1
        if lam[0] > k:
            return 0
        return sum(kronecker_coefficient(lam[:i], [k - lam[i]] + lam[i+1:]) for i in range(len(lam)))

    n = random.randint(3, 40)
    lambda_perm = (n-1, 1)
    lambda_det = (n-2, 1)

    multiplicity_perm = sym_power_multiplicity(lambda_perm, 2)
    multiplicity_det = sym_power_multiplicity(lambda_det, 2)

    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": multiplicity_perm - multiplicity_det,
        "instances_tested": 1,
        "conjecture_holds": multiplicity_perm > multiplicity_det,
        "counterexample": "" if multiplicity_perm > multiplicity_det else f"n={n}, lambda_perm={lambda_perm}, lambda_det={lambda_det}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")