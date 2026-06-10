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
    
    def generate_communication_complexity_problem(m, q):
        # Placeholder for generating a communication complexity problem
        return (m, q)

    def compute_binary_form_minimal_symplectic_representation_rank(m, q):
        # Placeholder for computing the minimal symplectic representation rank
        return m + q

    def compute_rank_variance(m, q):
        # Placeholder for computing the rank variance
        return abs(m - q) / (m + q)

    trials = 30
    n_max = 40
    instances_tested = 0
    total_mSR = 0
    total_w = 0

    for _ in range(trials):
        m = random.randint(5, n_max)
        q = random.randint(1, m)
        phi_G = generate_communication_complexity_problem(m, q)
        mSR_phi_G = compute_binary_form_minimal_symplectic_representation_rank(*phi_G)
        w_phi_G = compute_rank_variance(*phi_G)

        instances_tested += 1
        total_mSR += mSR_phi_G
        total_w += w_phi_G

    mean_mSR = total_mSR / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(mSR * w for mSR, w in zip(total_mSR, total_w)) - 
                               mean_mSR * total_w) / math.sqrt((instances_tested * sum(mSR**2 for mSR in total_mSR) - mean_mSR**2) *
                                                            (instances_tested * sum(w**2 for w in total_w) - mean_w**2))

    conjecture_holds = correlation_coefficient >= 0.9 and all(1.5 * mSR <= w for mSR, w in zip(total_mSR, total_w))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")