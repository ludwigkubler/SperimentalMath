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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def barycentric_coordinates(circuit):
        n = int(math.log2(len(circuit)))
        if 2**n != len(circuit):
            raise ValueError("Circuit length must be a power of 2")
        
        coordinates = set()
        for i in range(1, 2**n):
            for j in range(n):
                if circuit[i & (1 << j)] == 1:
                    coordinates.add(j)
        return len(coordinates)

    def entanglement_complexity(circuit):
        n = int(math.log2(len(circuit)))
        # Simplified heuristic for entanglement complexity
        return sum(1 for i in range(1, 2**n) if circuit[i] == 1)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            circuit = generate_circuit(n)
            bc = barycentric_coordinates(circuit)
            ec = entanglement_complexity(circuit)
            total_metric_value += abs(bc - ec) / max(bc, ec)
            instances_tested += 1
            n_max = max(n_max, n)

    metric_value = total_metric_value / instances_tested
    conjecture_holds = all(-0.2 <= (bc - ec) / max(bc, ec) <= 0.2 for bc, ec in zip(barycentric_coordinates(generate_circuit(n)) for n in n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "BC/EC Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs((bc - ec) / max(bc, ec)) > 0.2 for bc, ec in zip(barycentric_coordinates(generate_circuit(n)) for n in [5, 10, 15, 20, 30, 40])):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")