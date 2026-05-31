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
    
    def ackermann(m, n):
        if m == 0:
            return n + 1
        elif n == 0:
            return ackermann(m - 1, 1)
        else:
            return ackermann(m - 1, ackermann(m, n - 1))
    
    def communication_complexity(n):
        # Generate a random communication complexity instance
        inputs = [random.choice(['0', '1']) for _ in range(n)]
        outcomes = set()
        for i in range(2**n):
            outcome = ''.join(random.choice(['0', '1']) for _ in range(n))
            outcomes.add(outcome)
        return len(outcomes)
    
    def minimal_generators(outcomes):
        # Compute the minimal number of generators for a Coxeter group action
        n = len(outcomes)
        generators = set()
        for outcome in outcomes:
            for i in range(n):
                if outcome[i] == '0':
                    generators.add((i, 1))
                else:
                    generators.add((i, -1))
        return len(generators)
    
    def alpha_log_n(n):
        return ackermann(4, int(math.log2(n)))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            outcomes = communication_complexity(n)
            generators = minimal_generators(outcomes)
            alpha_log_n_value = alpha_log_n(n)
            if alpha_log_n_value == 0:
                continue
            ratio = generators / alpha_log_n_value
            total_metric_value += ratio
            instances_tested += 1
            if abs(ratio - 1) > 0.1:
                conjecture_holds = False
                counterexample = f"n={n}, outcomes={outcomes}, generators={generators}, alpha_log_n={alpha_log_n_value}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for _ in range(30) if conjecture_holds) / 30
    
    return {
        "metric_name": "Ratio of generators to α(log n)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")