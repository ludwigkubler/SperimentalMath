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

def generate_random_circuit(n):
    if n == 1:
        return ['NOT']
    else:
        gates = ['AND', 'OR', 'XOR']
        gate = random.choice(gates)
        inputs = [generate_random_circuit(random.randint(1, n//2)) for _ in range(2)]
        return [gate] + inputs

def count_gates(circuit):
    if isinstance(circuit[0], list):
        return sum(count_gates(subcircuit) for subcircuit in circuit[1:])
    else:
        return 1

def frobenius_schur_index(circuit):
    # Simplified approximation of Frobenius-Schur index
    width = count_gates(circuit)
    if width == 0:
        return 0
    return (width + 1) / (2 * width)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    fs_index_sum = 0
    width_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            fs_index = frobenius_schur_index(circuit)
            width = count_gates(circuit)
            fs_index_sum += fs_index
            width_sum += width
            instances_tested += 1
            n_max = max(n_max, n)

    mean_fs_index = fs_index_sum / instances_tested
    mean_width = width_sum / instances_tested

    correlation_coefficient = (instances_tested * sum(fs_index * width for fs_index, width in zip(fs_index_list, width_list)) -
                               sum(fs_index_list) * sum(width_list)) / \
                              math.sqrt((instances_tested * sum(fs_index**2 for fs_index in fs_index_list) - sum(fs_index_list)**2) *
                                        (instances_tested * sum(width**2 for width in width_list) - sum(width_list)**2))

    conjecture_holds = correlation_coefficient > 0.7 and abs(mean_fs_index - mean_width) <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_diff=<{}>".format(correlation_coefficient, abs(mean_fs_index - mean_width))

    return {
        "metric_name": "Frobenius-Schur Index vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for res in results if not res["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=%s first_failing_seed=%d" % (result["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE support_fraction=%.2f" % support_fraction)