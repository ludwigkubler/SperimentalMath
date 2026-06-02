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
    
    def generate_random_circuit(n):
        if n == 1:
            return ["A"]
        else:
            left = generate_random_circuit(n // 2)
            right = generate_random_circuit(n - n // 2)
            op = random.choice(["AND", "OR"])
            return [op, left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        else:
            op, left, right = circuit
            if op == "AND":
                return evaluate_circuit(left) and evaluate_circuit(right)
            elif op == "OR":
                return evaluate_circuit(left) or evaluate_circuit(right)
    
    def truth_table(circuit, n):
        variables = list(range(n))
        table = []
        for i in range(2 ** n):
            assignment = {var: (i >> var) & 1 for var in variables}
            result = evaluate_circuit(circuit)
            table.append((assignment, result))
        return table
    
    def monotone_width(table):
        n = len(table[0][0])
        width = 0
        for i in range(n):
            count = 0
            for assignment, result in table:
                if assignment[i] == 1 and result == False:
                    count += 1
            width = max(width, count)
        return width
    
    def quasigroup_representation(table):
        n = len(table[0][0])
        elements = set()
        for assignment, result in table:
            elements.update(assignment.values())
        elements = sorted(list(elements))
        element_to_index = {e: i for i, e in enumerate(elements)}
        
        qg = [[None] * len(elements) for _ in range(len(elements))]
        for assignment, result in table:
            inputs = [element_to_index[assignment[var]] for var in range(n)]
            output = element_to_index[result]
            if qg[inputs[0]][inputs[1]] is None:
                qg[inputs[0]][inputs[1]] = output
            else:
                return None  # Non-deterministic quasigroup, not valid
        
        return qg
    
    def minimal_order(qg):
        n = len(qg)
        for order in range(1, n + 1):
            if is_valid_quasigroup(qg, order):
                return order
        return n
    
    def is_valid_quasigroup(qg, order):
        n = len(qg)
        for i in range(n):
            for j in range(n):
                if qg[i][j] >= n:
                    return False
        return True
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    table = truth_table(circuit, n)
    mon_w = monotone_width(table)
    
    if mon_w == 0:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "monotone_width_is_zero"
        }
    
    qg = quasigroup_representation(table)
    if qg is None:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "non_deterministic_quasigroup"
        }
    
    min_order = minimal_order(qg)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_order <= 2 * mon_w and min_order >= mon_w / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")