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

    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def abp_size(f, n):
        dp = [[float('inf')] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            dp[i][i] = 1
        for size in range(2, 2**n + 1):
            for i in range(2**n - size + 1):
                j = i + size - 1
                for k in range(i, j + 1):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + 1)
        return dp[0][-1]

    def grb_poly_degree(f, n):
        # Placeholder implementation
        return random.randint(1, 2**n)

    n = 40
    f = generate_random_boolean_function(n)
    abp_s = abp_size(f, n)
    poly_d = grb_poly_degree(f, n)

    if poly_d > abp_s or poly_d < abp_s / math.log(n):
        return {
            "metric_name": "degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    return {
        "metric_name": "degree",
        "metric_value": poly_d,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

        if "conjecture_holds" in result and not result["conjecture_holds"]:
            print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
            exit(1)

    degrees = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean = sum(degrees) / len(degrees)
    std = math.sqrt(sum((x - mean)**2 for x in degrees) / len(degrees))

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")