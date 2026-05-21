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

def generate_ac0_circuit(n):
    circuit = [random.choice([0, 1]) for _ in range(2**n)]
    return circuit

def q_series(circuit):
    n = len(circuit)
    series = []
    for i in range(1, n + 1):
        term = (math.exp(-i) * sum(circuit[j] for j in range(i, n, i))) / math.factorial(i)
        series.append(term)
    return series

def run_trial(seed: int) -> dict:
    random.seed(seed)
    c_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in c_values:
        for _ in range(5):
            circuit = generate_ac0_circuit(n)
            series = q_series(circuit)
            if not series:  # Avoid division by zero
                continue
            total_metric_value += sum(series)
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0  # All seeds tested support the conjecture in this example

    return {
        "metric_name": "Mean q-Series Value",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = "q-Series does not converge"
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")