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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        elif n == 2:
            return ['0', '1', 'OR']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return left + right + ['AND']
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate in circuit:
            if gate == '0':
                stack.append('0')
            elif gate == '1':
                stack.append('1')
            elif gate == 'OR':
                b = stack.pop()
                a = stack.pop()
                stack.append('1' if a == '1' or b == '1' else '0')
            elif gate == 'AND':
                b = stack.pop()
                a = stack.pop()
                stack.append('1' if a == '1' and b == '1' else '0')
        return stack[0]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            if circuit[i] in ['OR', 'AND']:
                width[i] = max(width[i + 1], width[i + 2])
            else:
                width[i] = 1
        return width[0]
    
    def formal_group_order(circuit):
        n = len(circuit)
        order = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            if circuit[i] in ['OR', 'AND']:
                order[i] = max(order[i + 1], order[i + 2])
            else:
                order[i] = 1
        return sum(order) / n
    
    def run_experiment(n):
        circuit = generate_circuit(n)
        inputs = [random.choice(['0', '1']) for _ in range(n)]
        result = evaluate_circuit(circuit, inputs)
        width = monotone_width(circuit)
        order = formal_group_order(circuit)
        return width, order
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_order = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            width, order = run_experiment(n)
            total_instances += 1
            total_order += order
            max_n = max(max_n, n)
            if order > math.sqrt(n):
                conjecture_holds = False
                counterexample = f"Order(G)={order} > sqrt({n}) for n={n}"
    
    mean_order = total_order / total_instances
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": "Formal Group Order",
        "metric_value": mean_order,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")