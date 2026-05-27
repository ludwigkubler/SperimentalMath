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

def generate_boolean_circuit(n):
    if n == 1:
        return "x0"
    else:
        left = generate_boolean_circuit(n // 2)
        right = generate_boolean_circuit(n - n // 2)
        return f"({left} AND {right}) OR ({left} AND NOT {right})"

def evaluate_circuit(circuit, valuation):
    if circuit.startswith('(') and circuit.endswith(')'):
        circuit = circuit[1:-1]
    if ' OR ' in circuit:
        left, right = circuit.split(' OR ')
        return evaluate_circuit(left, valuation) or evaluate_circuit(right, valuation)
    elif ' AND ' in circuit:
        left, right = circuit.split(' AND ')
        return evaluate_circuit(left, valuation) and evaluate_circuit(right, valuation)
    elif ' NOT ' in circuit:
        sub_circuit = circuit[5:]
        return not evaluate_circuit(sub_circuit, valuation)
    else:
        var, negated = circuit.startswith('NOT '), circuit[4:] if circuit.startswith('NOT ') else circuit
        return valuation[var] != (negated == '1')

def minimal_rank(valuation):
    rank = 0
    for key in valuation:
        if valuation[key]:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_boolean_circuit(n)
            valuation = {f"x{i}": random.choice([True, False]) for i in range(n)}
            if evaluate_circuit(circuit, valuation):
                total_rank += minimal_rank(valuation)
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_rank = total_rank / instances_tested
    expected_rank = math.log(n_values[-1])
    std_dev = math.sqrt(sum((rank - avg_rank) ** 2 for rank in range(5, 41)) / (n_values[-1] - 4))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(avg_rank - expected_rank) <= std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")