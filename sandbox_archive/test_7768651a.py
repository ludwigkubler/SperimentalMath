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
            lit = expr.split()[1]
            if lit not in values:
                values[lit] = random.choice(['0', '1'])
            result = eval(expr.replace('AND', '&').replace('OR', '|'), {'__builtins__': None}, values)
            values[expr] = str(result)
        return values[circuit[-1]]

def p_adic_valuation(circuit):
    values = evaluate_circuit(circuit)
    max_val = 0
    for val in values.values():
        if val == '1':
            max_val += 1
    return max_val

def monotone_width(circuit):
    queue = [circuit]
    visited = set()
    width = 0
    while queue:
        next_queue = []
        for expr in queue:
            if expr not in visited:
                visited.add(expr)
                if isinstance(expr, list):
                    left, right = expr[1], expr[3]
                    next_queue.extend([left, right])
        queue = next_queue
        width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_circuit(n)
        v_p = p_adic_valuation(circuit)
        w_mon = monotone_width(circuit)
        if v_p == 0 or w_mon == 0:
            continue
        results.append((n, v_p, w_mon))
    if not results:
        return {
            "metric_name": "monotone_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    v_p_values = [v_p for _, v_p, _ in results]
    w_mon_values = [w_mon for _, _, w_mon in results]
    mean_v_p = sum(v_p_values) / instances_tested
    mean_w_mon = sum(w_mon_values) / instances_tested
    std_v_p = (sum((v_p - mean_v_p) ** 2 for v_p in v_p_values) / instances_tested) ** 0.5
    std_w_mon = (sum((w_mon - mean_w_mon) ** 2 for w_mon in w_mon_values) / instances_tested) ** 0.5
    support_fraction = sum(1 for _, _, w_mon in results if w_mon <= 1.5 * mean_v_p ** 2 * n_max) / instances_tested
    return {
        "metric_name": "monotone_width",
        "metric_value": mean_w_mon,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"monotone_width > 1.5 * v(p)^2 * {n_max}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"monotone_width > 1.5 * v(p)^2 * {r['n_max']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")