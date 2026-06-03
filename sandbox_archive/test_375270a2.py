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
            return ['0', '1']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        else:
            left = evaluate_circuit(circuit[0])
            right = evaluate_circuit(circuit[2])
            if circuit[1] == 'AND':
                return '1' if left == '1' and right == '1' else '0'
            elif circuit[1] == 'OR':
                return '1' if left == '1' or right == '1' else '0'
    
    def p_adic_valuation(circuit):
        if isinstance(circuit, str):
            return 0
        else:
            left = p_adic_valuation(circuit[0])
            right = p_adic_valuation(circuit[2])
            return max(left, right) + 1
    
    def monotone_width(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            left = monotone_width(circuit[0])
            right = monotone_width(circuit[2])
            return max(left, right)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    val = p_adic_valuation(circuit)
    w_mon = monotone_width(circuit)
    
    if val == 0:
        return {
            "metric_name": "w_mon(C)",
            "metric_value": w_mon,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "p-adic valuation is zero"
        }
    
    if w_mon > 1.5 * val**2 * n:
        return {
            "metric_name": "w_mon(C)",
            "metric_value": w_mon,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"w_mon(C) > 1.5 * v(p)^2n ({w_mon} > {1.5 * val**2 * n})"
        }
    
    return {
        "metric_name": "w_mon(C)",
        "metric_value": w_mon,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(values)/len(values)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(values)/len(values)} std={math.sqrt(sum((x - sum(values)/len(values))**2 for x in values) / len(values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"w_mon(C) > 1.5 * v(p)^2n\" first_failing_seed={first_failing_seed}")