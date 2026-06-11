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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def cnf_to_quandle(cnf):
        n = len(cnf[0])
        quandle = [[Fraction(0, 1)] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row = quandle[literal - 1]
                    col = quandle[-literal - 1]
                    row[elements.index(literal)] += Fraction(1, 1)
                    col[elements.index(-literal)] += Fraction(1, 1)
        return quandle
    
    def quandle_order(quandle):
        n = len(quandle)
        for i in range(n):
            for j in range(n):
                if quandle[i][j] != quandle[j][i]:
                    return max(sum(row) for row in quandle)
        return sum(max(row) for row in quandle)
    
    def entanglement_width(cnf):
        width = 0
        for clause in cnf:
            literals = set(abs(lit) for lit in clause)
            if len(literals) > width:
                width = len(literals)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf_size = random.randint(2, min(n * (n - 1) // 2, 40))
        cnf = [[random.choice([-i, i]) for _ in range(random.randint(2, min(n, 5)))] for _ in range(cnf_size)]
        quandle = cnf_to_quandle(cnf)
        min_order = quandle_order(quandle)
        entanglement_width_val = entanglement_width(cnf)
        
        results.append({
            "n": n,
            "cnf_size": cnf_size,
            "min_order": min_order,
            "entanglement_width": entanglement_width_val
        })
    
    if not results:
        return {
            "metric_name": "MinOrder vs EntanglementWidth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    min_order_values = [r["min_order"] for r in results]
    entanglement_width_values = [r["entanglement_width"] for r in results]
    
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_entanglement_width = sum(entanglement_width_values) / len(entanglement_width_values)
    
    correlation_coefficient = 0
    if len(min_order_values) > 1:
        numerator = sum((min_order_values[i] - mean_min_order) * (entanglement_width_values[i] - mean_entanglement_width) for i in range(len(min_order_values)))
        denominator = (sum((min_order_values[i] - mean_min_order)**2 for i in range(len(min_order_values))) * sum((entanglement_width_values[i] - mean_entanglement_width)**2 for i in range(len(entanglement_width_values))))**0.5
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "MinOrder vs EntanglementWidth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_order_values),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    min_order_values = [run_trial(seed)["min_order"] for seed in seeds if run_trial(seed)["instances_tested"] > 0]
    entanglement_width_values = [run_trial(seed)["entanglement_width"] for seed in seeds if run_trial(seed)["instances_tested"] > 0]
    
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_entanglement_width = sum(entanglement_width_values) / len(entanglement_width_values)
    
    correlation_coefficient = 0
    if len(min_order_values) > 1:
        numerator = sum((min_order_values[i] - mean_min_order) * (entanglement_width_values[i] - mean_entanglement_width) for i in range(len(min_order_values)))
        denominator = (sum((min_order_values[i] - mean_min_order)**2 for i in range(len(min_order_values))) * sum((entanglement_width_values[i] - mean_entanglement_width)**2 for i in range(len(entanglement_width_values))))**0.5
        correlation_coefficient = numerator / denominator
    
    support_fraction = sum(1 for seed in seeds if run_trial(seed)["conjecture_holds"]) / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={sum((x - mean_min_order)**2 for x in min_order_values) ** 0.5} support_fraction={support_fraction}")
    elif any(not run_trial(seed)["conjecture_holds"] for seed in seeds):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient does not meet the threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")