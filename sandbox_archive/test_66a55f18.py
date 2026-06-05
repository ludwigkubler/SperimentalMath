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
    
    def generate_d_regular_circuit(d, n):
        if d * (n - 1) % (d + 1) != 0:
            return None
        circuit = [random.choice([0, 1]) for _ in range(n)]
        while True:
            valid = True
            for i in range(1, n):
                if sum(circuit[j] for j in range(i)) % (d + 1) != circuit[i]:
                    valid = False
                    break
            if valid:
                return circuit
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            width = max(width, sum(1 for j in range(i + 1) if circuit[j] == 1))
        return width
    
    def tropical_module_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            rank += circuit[i]
        return rank
    
    d_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for d in d_values:
        n = random.randint(5, 40)
        circuit = generate_d_regular_circuit(d, n)
        if circuit is None:
            continue
        mtr = tropical_module_rank(circuit)
        width = monotone_width(circuit)
        results.append((mtr, width))
    
    if not results:
        return {
            "metric_name": "monotone_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mtr_values = [mtr for mtr, _ in results]
    width_values = [width for _, width in results]
    avg_mtr = sum(mtr_values) / len(mtr_values)
    avg_width = sum(width_values) / len(width_values)
    std_dev = math.sqrt(sum((x - avg_mtr) ** 2 for x in mtr_values) / len(mtr_values))
    
    conjecture_holds = all(abs(mtr - width) <= 0.5 * (d ** 0.5 * n ** (1/3)) for mtr, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "monotone_width",
        "metric_value": avg_mtr,
        "instances_tested": len(results),
        "n_max": max(len(circuit) for _, circuit in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(mtr - width) > 0.5 * (d ** 0.5 * n ** (1/3)) for mtr, width, d, n in zip([r["metric_value"] for r in results], [r["instances_tested"] for r in results], [r["n_max"] for r in results])):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")