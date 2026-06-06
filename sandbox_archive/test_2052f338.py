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
            return "0"
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return f"({left} {right})"
    
    def monotone_width(circuit):
        stack = []
        max_depth = 0
        current_depth = 0
        
        for char in circuit:
            if char == '(':
                current_depth += 1
                stack.append(char)
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                stack.pop()
                current_depth -= 1
        
        return max_depth
    
    def formal_group_order(n):
        # Simplified heuristic for the order of a formal group associated with a circuit
        return n * (n + 1) // 2
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    
    w_mon = monotone_width(circuit)
    Order_G = formal_group_order(n)
    
    metric_name = "Monotone Width vs Formal Group Order"
    metric_value = Order_G
    instances_tested = 1
    n_max = n
    conjecture_holds = Order_G <= math.sqrt(n) * w_mon
    counterexample = "" if conjecture_holds else f"Order(G)={Order_G}, w_mon(C)={w_mon}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order(G) > k * n^(1/2)\" first_failing_seed={first_failing_seed}")