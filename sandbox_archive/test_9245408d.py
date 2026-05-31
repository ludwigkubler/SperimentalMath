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

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_instance(n):
        inputs = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
        outcomes = [random.randint(0, 1) for _ in range(2**n)]
        return inputs, outcomes

    def compute_minimal_generators(inputs, outcomes):
        n = len(inputs[0])
        generators = set()
        for outcome in outcomes:
            generator = []
            for i in range(n):
                if outcome & (1 << i):
                    generator.append(i)
            generators.add(tuple(sorted(generator)))
        return len(generators)

    def alpha(log_n):
        if log_n == 0:
            return 1
        elif log_n == 1:
            return 2
        else:
            a = 2
            for _ in range(1, log_n):
                a = 2 ** a
            return a

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        inputs, outcomes = generate_communication_instance(n)
        min_generators = compute_minimal_generators(inputs, outcomes)
        alpha_log_n = alpha(int(math.log2(n)))
        metric_value = Fraction(min_generators, alpha_log_n)

        total_metric_value += metric_value
        instances_tested += len(outcomes)
        n_max = max(n_max, n)

        if abs(metric_value - 1) > Fraction(10, 100):
            conjecture_holds = False
            counterexample = f"n={n}, min_generators={min_generators}, alpha_log_n={alpha_log_n}"

    mean_metric_value = total_metric_value / instances_tested

    return {
        "metric_name": "minimal_generators_over_alpha_log_n",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")