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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_circuit(f):
        n = len(f)
        circuit = []
        for i in range(n):
            if f[i] == 1:
                circuit.append((i,))
            else:
                circuit.append((i, i))
        return circuit
    
    def p_adic_divergence(circuit):
        n = len(circuit)
        count = [0] * (n + 1)
        for gate in circuit:
            if len(gate) == 2:
                count[gate[0]] += 1
                count[gate[1]] += 1
            else:
                count[gate[0]] += 1
        total = sum(count)
        return Fraction(sum(x * x for x in count), total * total)
    
    def communication_complexity(circuit):
        n = len(circuit)
        rank = [0] * (n + 1)
        for gate in circuit:
            if len(gate) == 2:
                rank[gate[0]] += 1
                rank[gate[1]] += 1
            else:
                rank[gate[0]] += 1
        return sum(rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        c_f = construct_circuit(f)
        min_d_f = p_adic_divergence(c_f)
        c_f = communication_complexity(c_f)
        results.append((min_d_f, c_f))
    
    if len(results) < 30:
        return {
            "metric_name": "p-adic divergence vs communication complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    min_d_values = [r[0] for r in results]
    c_f_values = [r[1] for r in results]
    
    mean_min_d = sum(min_d_values) / len(min_d_values)
    std_min_d = math.sqrt(sum((x - mean_min_d)**2 for x in min_d_values) / len(min_d_values))
    mean_c_f = sum(c_f_values) / len(c_f_values)
    std_c_f = math.sqrt(sum((x - mean_c_f)**2 for x in c_f_values) / len(c_f_values))
    
    correlation_coefficient = (sum((min_d_values[i] - mean_min_d) * (c_f_values[i] - mean_c_f) for i in range(len(min_d_values))) /
                               (len(min_d_values) * std_min_d * std_c_f))
    
    if abs(correlation_coefficient) >= 0.7 and abs(mean_min_d - mean_c_f) <= 3:
        return {
            "metric_name": "p-adic divergence vs communication complexity",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "p-adic divergence vs communication complexity",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"correlation={correlation_coefficient}, mean_diff={abs(mean_min_d - mean_c_f)}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break