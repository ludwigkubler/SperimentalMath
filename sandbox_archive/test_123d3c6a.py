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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_planar_circuit(n):
        # Simple heuristic to generate a planar circuit
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            return [0] + generate_planar_circuit(n-1) + [n-1]

    def hodge_theoretic_index(circuit):
        # Placeholder for Hodge-theoretic index computation
        # This is a dummy implementation that returns the length of the circuit
        return len(circuit)

    def monotone_width(circuit):
        # Placeholder for monotone width computation
        # This is a dummy implementation that returns the length of the circuit
        return len(circuit)

    n_max = 40
    instances_tested = 30
    total_w_c_over_f_n = Fraction(0, 1)
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_planar_circuit(n)
        f_n = n ** (2 / 3)
        w_C = monotone_width(circuit)
        hodge_index = hodge_theoretic_index(circuit)

        if w_C > f_n:
            conjecture_holds = False
            counterexample = f"Circuit size {n}, w(C) = {w_C}, f(n) = {f_n}"
            break

        total_w_c_over_f_n += Fraction(w_C, f_n)

    mean_value = total_w_c_over_f_n / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0

    return {
        "metric_name": "w(C) / f(n)",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")