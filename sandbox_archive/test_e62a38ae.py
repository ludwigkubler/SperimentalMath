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
        results = [evaluate_circuit(subcircuit) for subcircuit in circuit]
        return '1' if any(result == '1' for result in results) else '0'

def p_adic_valuation(circuit):
    if isinstance(circuit, str):
        return 0
    else:
        return max(p_adic_valuation(subcircuit) for subcircuit in circuit)

def monotone_width(circuit):
    if isinstance(circuit, str):
        return 1
    else:
        left_width = monotone_width(circuit[0])
        right_width = monotone_width(circuit[2])
        return max(left_width + 1, right_width + 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        v_p = p_adic_valuation(circuit)
        w_mon = monotone_width(circuit)
        results.append((v_p, w_mon))
        
        if len(results) >= 30:
            break
    
    total_v_p = sum(v_p for v_p, _ in results)
    total_w_mon = sum(w_mon for _, w_mon in results)
    mean_v_p = total_v_p / len(results)
    mean_w_mon = total_w_mon / len(results)
    
    conjecture_holds = all(w_mon <= 1.5 * v_p**2 * n for v_p, w_mon, n in zip(results, results, n_values))
    counterexample = "" if conjecture_holds else "n/a"
    
    return {
        "metric_name": "Monotone Width vs p-Adic Valuation",
        "metric_value": mean_w_mon,
        "instances_tested": len(results),
        "n_max": max(n for _, _, n in results),
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n/a' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")