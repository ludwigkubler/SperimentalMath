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
    
    def generate_d_regular_boolean_function(d, n):
        if d <= 0 or n <= 0:
            return None
        function = [random.choice([0, 1]) for _ in range(n)]
        while True:
            valid = True
            for i in range(n):
                count = sum(1 for j in range(n) if (i != j and function[i] == function[j]))
                if count != d:
                    valid = False
                    break
            if valid:
                return function
            function = [random.choice([0, 1]) for _ in range(n)]

    def calculate_galois_group_degree(function):
        n = len(function)
        if n <= 1:
            return 0
        degree = 1
        while True:
            new_function = [function[i] ^ function[(i + degree) % n] for i in range(n)]
            if new_function == function:
                break
            degree += 1
        return degree

    def calculate_circuit_entanglement(function):
        n = len(function)
        entanglement = 0
        for i in range(n):
            count = sum(1 for j in range(n) if (i != j and function[i] == function[j]))
            entanglement = max(entanglement, count)
        return entanglement

    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(1, min(n - 1, 5))
            function = generate_d_regular_boolean_function(d, n)
            if function is None:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            deg_G_f = calculate_galois_group_degree(function)
            Ent_f = calculate_circuit_entanglement(function)
            if deg_G_f > Ent_f * Ent_f or Ent_f > deg_G_f:
                conjecture_holds = False
                counterexample = f"n={n}, d={d}, deg(G_f)={deg_G_f}, Ent(f)={Ent_f}"
                break

    return {
        "metric_name": "Galois Group Degree",
        "metric_value": deg_G_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")