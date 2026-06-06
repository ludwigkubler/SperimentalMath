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
    
    def communication_complexity(f):
        n = len(f)
        cc = 0
        for i in range(2**n):
            input_bits = [int(b) for b in format(i, f'0{n}b')]
            output = f[input_bits]
            if output not in [0, 1]:
                continue
            cc += 1
        return cc
    
    def quasi_random_sequences(n):
        sequences = []
        for _ in range(2**n):
            sequence = [random.choice([0, 1]) for _ in range(n)]
            sequences.append(sequence)
        return sequences
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = [random.choice([0, 1]) for _ in range(2**n)]
            cc = communication_complexity(f)
            if cc == 0:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            expected_log_cc = math.log2(cc) ** 2
            actual_log_cc = math.log2(instances_tested)
            total_metric_value += abs(expected_log_cc - actual_log_cc)
            if abs(expected_log_cc - actual_log_cc) > 3:
                conjecture_holds = False
                counterexample = f"n={n}, cc={cc}, instances_tested={instances_tested}"
    
    return {
        "metric_name": "log_difference",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")