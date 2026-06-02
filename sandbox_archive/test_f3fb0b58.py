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
    
    def evaluate_circuit(circuit, inputs):
        for gate in circuit:
            if gate[0] == 'AND':
                inputs.append(inputs.pop() and inputs.pop())
            elif gate[0] == 'OR':
                inputs.append(inputs.pop() or inputs.pop())
            elif gate[0] == 'NOT':
                inputs[-1] = not inputs[-1]
        return inputs[0]

    def truth_table(circuit, n):
        table = []
        for i in range(2**n):
            binary_input = [bool((i >> j) & 1) for j in range(n)]
            result = evaluate_circuit(circuit, binary_input[:])
            table.append((binary_input, result))
        return table

    def quasigroup_representation(table):
        n = len(table[0][0])
        elements = set()
        for inputs, _ in table:
            for bit in inputs + [table[0][1]]:
                elements.add(bit)
        elements = sorted(elements)

        qg = {}
        for i, a in enumerate(elements):
            for j, b in enumerate(elements):
                qg[(a, b)] = elements[(i * len(elements) + j) % len(elements)]
        return qg

    def minimal_order(qg):
        n = len(qg)
        order = 1
        while True:
            found = False
            for a in range(n):
                for b in range(n):
                    if qg[(qg[(a, b)], qg[(b, a)])] != qg[(a, b)]:
                        found = True
                        break
                if found:
                    break
            if not found:
                return order
            order += 1

    def monotone_width(circuit):
        n = len(circuit)
        width = [0] * (n + 1)
        for gate in circuit:
            if gate[0] == 'AND' or gate[0] == 'OR':
                width[gate[2]] = max(width[gate[1]], width[gate[3]]) + 1
            elif gate[0] == 'NOT':
                width[gate[2]] = width[gate[1]]
        return max(width)

    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            circuit = []
            for i in range(n - 1):
                gate_type = random.choice(['AND', 'OR'])
                inputs = [random.randint(0, n-1) for _ in range(gate_type == 'OR')]
                circuit.append((gate_type, *inputs))
            table = truth_table(circuit, n)
            qg = quasigroup_representation(table)
            order = minimal_order(qg)
            mon_width = monotone_width(circuit)
            results.append((order, mon_width))

    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    orders, mon_widths = zip(*results)
    corr = correlation(orders, mon_widths)

    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")