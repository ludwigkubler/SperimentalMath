# auto-injected by SEC sandbox
import math
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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for r in right]

def evaluate_circuit(circuit):
    if isinstance(circuit, str):
        return circuit
    else:
        values = {}
        for expr in circuit:
            parts = expr.split()
            if len(parts) == 3 and parts[1] in ['AND', 'OR']:
                left = evaluate_circuit(parts[0])
                right = evaluate_circuit(parts[2])
                if parts[1] == 'AND':
                    values[expr] = left and right
                else:
                    values[expr] = left or right
        return values[circuit[-1]]

def p_adic_valuation(circuit):
    def count_ones(expr):
        if isinstance(expr, str):
            return expr.count('1')
        else:
            return sum(count_ones(part) for part in expr)
    
    return count_ones(evaluate_circuit(circuit))

def monotone_width(circuit):
    def is_monotone(expr):
        if isinstance(expr, str):
            return True
        else:
            left = is_monotone(expr[0])
            right = is_monotone(expr[2])
            return left and right
    
    def count_nodes(expr):
        if isinstance(expr, str):
            return 1
        else:
            return 1 + count_nodes(expr[0]) + count_nodes(expr[2])
    
    return count_nodes(evaluate_circuit(circuit)) if is_monotone(evaluate_circuit(circuit)) else float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    v_p = p_adic_valuation(circuit)
    w_mon = monotone_width(circuit)
    
    if v_p == 0:
        return {
            "metric_name": "w_mon(C) / v(p)^2n",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "v(p) = 0, undefined"
        }
    
    metric_value = w_mon / (v_p ** 2 * n)
    conjecture_holds = metric_value <= 1.5
    counterexample = "" if conjecture_holds else f"w_mon(C) = {w_mon}, v(p)^2n = {v_p**2*n}"
    
    return {
        "metric_name": "w_mon(C) / v(p)^2n",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"w_mon(C) > 1.5 * v(p)^2n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")