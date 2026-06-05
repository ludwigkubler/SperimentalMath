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
    
    def generate_random_monotone_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            output = random.randint(0, 1)
            circuit.append((gate_type, inputs, output))
        return circuit
    
    def construct_cocomplex(circuit):
        cocomplex = {}
        for gate_type, inputs, output in circuit:
            if gate_type == 'AND':
                for i in range(len(inputs)):
                    for j in range(i + 1, len(inputs)):
                        key = (inputs[i], inputs[j])
                        if key not in cocomplex:
                            cocomplex[key] = set()
                        cocomplex[key].add(output)
            elif gate_type == 'OR':
                for i in range(len(inputs)):
                    key = (inputs[i],)
                    if key not in cocomplex:
                        cocomplex[key] = set()
                    cocomplex[key].add(output)
        return cocomplex
    
    def min_rank(cocomplex):
        keys = list(cocomplex.keys())
        n = len(keys)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(cocomplex[keys[i]].intersection(cocomplex[keys[j]])):
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for j in range(n):
                    if row[j]:
                        for k in range(n):
                            matrix[k][j] = (matrix[k][j] + matrix[k][i]) % 2
        return rank
    
    def monotone_width(circuit):
        width = 0
        for gate_type, inputs, output in circuit:
            if gate_type == 'AND':
                width += len(inputs)
            elif gate_type == 'OR':
                width += 1
        return width
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        circuit = generate_random_monotone_circuit(random.randint(5, 40))
        cocomplex = construct_cocomplex(circuit)
        mrank = min_rank(cocomplex)
        w_mon = monotone_width(circuit)
        
        metric_values.append((mrank, w_mon))
    
    mean_mrank = sum(m for m, _ in metric_values) / len(metric_values)
    mean_w_mon = sum(w for _, w in metric_values) / len(metric_values)
    abs_diff_sum = sum(abs(m - w) for m, w in metric_values)
    avg_abs_diff = abs_diff_sum / len(metric_values)
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        numerator = sum((m - mean_mrank) * (w - mean_w_mon) for m, w in metric_values)
        denominator = math.sqrt(sum((m - mean_mrank) ** 2 for m, _ in metric_values)) * math.sqrt(sum((w - mean_w_mon) ** 2 for _, w in metric_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and avg_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> avg_abs_diff=<{}>".format(correlation_coefficient, avg_abs_diff)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) >= len(results) * 0.2:
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]["counterexample"], seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")