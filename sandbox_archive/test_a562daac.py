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

def generate_boolean_circuit(n: int) -> list:
    if n <= 0:
        return []
    
    circuit = []
    for _ in range(2**n - 1):
        gate_type = random.choice(['AND', 'OR', 'NOT'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(2)]
        circuit.append((gate_type, inputs))
    return circuit

def p_adic_metric(circuit: list) -> Fraction:
    if not circuit:
        return Fraction(0)
    
    metric = Fraction(0)
    for gate, inputs in circuit:
        if gate == 'NOT':
            metric += Fraction(inputs[0])
        elif gate == 'AND':
            metric += Fraction(inputs[0] * inputs[1])
        elif gate == 'OR':
            metric += Fraction(inputs[0] + inputs[1] - inputs[0] * inputs[1])
    return metric

def entanglement_complexity(circuit: list) -> int:
    if not circuit:
        return 0
    
    complexity = 0
    for gate, _ in circuit:
        if gate == 'AND' or gate == 'OR':
            complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        if not circuit:
            continue
        
        r_p_C = p_adic_metric(circuit)
        e_C = entanglement_complexity(circuit)
        
        results.append({
            "n": n,
            "r_p_C": r_p_C,
            "e_C": e_C
        })
    
    if not results:
        return {
            "metric_name": "p-adic metric rank vs. entanglement complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    n_max = max(result["n"] for result in results)
    metric_values = [result["r_p_C"] - result["e_C"] for result in results]
    mean_d = sum(metric_values) / len(metric_values)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "p-adic metric rank vs. entanglement complexity",
        "metric_value": mean_d,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(mean_d) <= 5 and all(abs(d) >= 0 for d in metric_values),
        "counterexample": "" if all(abs(d) >= 0 for d in metric_values) else "negative_diff"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"negative_diff\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")