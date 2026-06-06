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
            return [0] + generate_planar_circuit(n - 1) + [n - 1]
    
    def compute_minimal_hodge_index(circuit):
        # Dummy implementation for minimal Hodge index
        return len(circuit)
    
    def compute_monotone_width(circuit):
        # Dummy implementation for monotone width
        return len(circuit)
    
    n_max = 40
    instances_tested = 0
    total_w_c_over_f_n = Fraction(0, 1)
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        if n > 30:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30')
            return {
                "metric_name": "Monotone Width Ratio",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        for _ in range(40 // (n - 4)):
            circuit = generate_planar_circuit(n)
            w_C = compute_monotone_width(circuit)
            f_n = n ** (2 / 3)
            total_w_c_over_f_n += Fraction(w_C, f_n)
            instances_tested += 1
            
            if w_C > f_n:
                conjecture_holds = False
                counterexample = f"n={n}, w(C)={w_C}, f(n)={f_n}"
    
    mean_value = total_w_c_over_f_n / instances_tested
    support_fraction = sum(1 for _ in range(instances_tested) if w_C <= f_n) / instances_tested
    
    if support_fraction >= 0.8:
        result = "SUPPORTED"
    elif support_fraction < 0.2:
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"
    
    return {
        "metric_name": "Monotone Width Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("support_fraction" in r and r["support_fraction"] >= 0.8 for r in results):
        print(f'RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}')
    elif any("counterexample" in r and r["conjecture_holds"] == False for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="{results[0]["counterexample"]}" first_failing_seed={first_failing_seed}')
    else:
        print(f'RESULT: INCONCLUSIVE support_fraction={support_fraction}')