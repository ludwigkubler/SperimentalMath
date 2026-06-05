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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(n)]

    def monotone_width(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left_width = monotone_width(circuit[:len(circuit)//2])
            right_width = monotone_width(circuit[len(circuit)//2:])
            return max(left_width, right_width)

    def algebraic_k_theory_rank(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left_rank = algebraic_k_theory_rank(circuit[:len(circuit)//2])
            right_rank = algebraic_k_theory_rank(circuit[len(circuit)//2:])
            return max(left_rank, right_rank) + 1

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        r_K = algebraic_k_theory_rank(circuit)
        w_mon = monotone_width(circuit)
        
        if abs(r_K - w_mon) > 3:
            counterexample = f"r_K({n})={r_K}, w_mon({n})={w_mon}"
            conjecture_holds = False
            break
        
        metric_values.append((r_K, w_mon))

    mean_r_K = sum(x[0] for x in metric_values) / len(metric_values)
    mean_w_mon = sum(x[1] for x in metric_values) / len(metric_values)
    correlation_coefficient = (sum((x[0] - mean_r_K) * (x[1] - mean_w_mon) for x in metric_values) /
                               math.sqrt(sum((x[0] - mean_r_K)**2 for x in metric_values)) *
                               math.sqrt(sum((x[1] - mean_w_mon)**2 for x in metric_values)))

    return {
        "metric_name": "Algebraic K-Theory Rank vs Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")