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
            return [0, 1]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [left[i] ^ right[i] for i in range(n)]
    
    def compute_semigroup(circuit):
        n = len(circuit)
        semigroup = {0}
        for _ in range(1, 2**n):
            new_elements = set()
            for x in semigroup:
                for y in circuit:
                    new_elements.add(x ^ y)
            semigroup.update(new_elements)
        return len(semigroup)
    
    def compute_circuitmonowidth(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_semgroup_order = 0
    total_circuitmonowidth = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            semigroup_order = compute_semigroup(circuit)
            circuitmonowidth = compute_circuitmonowidth(circuit)
            instances_tested += 1
            total_semgroup_order += semigroup_order
            total_circuitmonowidth += circuitmonowidth
    
    if instances_tested < 30:
        return {
            "metric_name": "Semigroup Order / Circuit Monotone Width Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    avg_semgroup_order = total_semgroup_order / instances_tested
    avg_circuitmonowidth = total_circuitmonowidth / instances_tested
    ratio = avg_semgroup_order / avg_circuitmonowidth
    
    return {
        "metric_name": "Semigroup Order / Circuit Monotone Width Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Ratio: {ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    avg_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 1\" first_failing_seed={first_failing_seed}")