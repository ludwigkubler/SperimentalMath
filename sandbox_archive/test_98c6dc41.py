# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def tropical_max(a, b):
        return max(a, b)

    def tropical_min(a, b):
        return min(a, b)

    def discrete_tropical_fourier_transform(f, N):
        n = len(f)
        h = [-math.inf] * n
        for k in range(n):
            for x in range(n):
                h[k] = tropical_max(h[k], f[x] - 2 * math.pi * k * x / n)
        return h

    def minimal_fourier_coefficient(h):
        return min(h)

    def discrepancy_calculation(f):
        mean = sum(f) / len(f)
        return max(f) - mean

    N_values = [8, 16, 32, 64]
    violations = 0
    total_slack = 0
    instances_tested = 0

    for N in N_values:
        C_N = math.log2(N)
        for _ in range(50):  # 50 trials per N
            f = [random.uniform(-10, 10) if random.random() < 0.9 else -math.inf for _ in range(N)]
            g = [random.uniform(-10, 10) if random.random() < 0.9 else -math.inf for _ in range(N)]

            h_f = discrete_tropical_fourier_transform(f, N)
            h_g = discrete_tropical_fourier_transform(g, N)
            h_fg = discrete_tropical_fourier_transform([tropical_max(f[i], g[i]) for i in range(N)], N)

            mfc_f = minimal_fourier_coefficient(h_f)
            mfc_g = minimal_fourier_coefficient(h_g)
            mfc_fg = minimal_fourier_coefficient(h_fg)

            disc_f = discrepancy_calculation(f)
            disc_g = discrepancy_calculation(g)
            disc_fg = discrepancy_calculation([tropical_max(f[i], g[i]) for i in range(N)])

            slack = abs(mfc_fg - min(mfc_f, mfc_g) + C_N)
            total_slack += slack
            instances_tested += 1

            if slack > C_N + 0.5:
                violations += 1

    mean_slack = total_slack / instances_tested
    support_fraction = (instances_tested - violations) / instances_tested

    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.99,
        "counterexample": "" if support_fraction >= 0.99 else f"Slack exceeded {C_N + 0.5} after {violations} violations"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.99")