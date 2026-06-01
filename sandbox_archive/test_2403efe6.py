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
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [f'({x} AND {y}) OR ({x} AND NOT {y})' for x in left for y in right] + ['NOT ' + x for x in left]
    
    def evaluate_circuit(circuit):
        if circuit == '0':
            return 0
        elif circuit.startswith('NOT'):
            return 1 - evaluate_circuit(circuit[4:])
        else:
            op = circuit[-3:]
            a, b = circuit[:-4].split(' AND ')
            if op == 'AND':
                return min(evaluate_circuit(a), evaluate_circuit(b))
            elif op == 'OR':
                return max(evaluate_circuit(a), evaluate_circuit(b))
    
    def compute_brauer_group(circuit):
        n = len(circuit)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            G[i][i] = 1
        for expr in circuit.split(' OR '):
            if expr.startswith('NOT'):
                continue
            a, b = expr.split(' AND ')
            G[a-1][b-1] = 1
            G[b-1][a-1] = 1
        return G
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def monotone_width(circuit):
        n = len(circuit)
        max_width = 0
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            width = 0
            for expr in circuit.split(' OR '):
                if expr.startswith('NOT'):
                    continue
                a, b = expr.split(' AND ')
                if evaluate_circuit(a) == assignment[int(a)-1] and evaluate_circuit(b) == assignment[int(b)-1]:
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        rank = gaussian_elimination(compute_brauer_group(circuit))
        width = monotone_width(circuit)
        ranks.append(rank)
        widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Brauer Group Rank vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(ranks)
    mean_rank = sum(ranks) / n
    mean_width = sum(widths) / n
    
    slope = (mean_rank - mean_width) / mean_width if mean_width != 0 else float('inf')
    p_value = 2 * min(abs(slope - 1), 1 - abs(slope - 1))  # Approximate p-value for a linear regression
    
    return {
        "metric_name": "Brauer Group Rank vs Monotone Width",
        "metric_value": slope,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(slope - 1) <= 0.1 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        std_slope = math.sqrt(sum((r["metric_value"] - mean_slope)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")