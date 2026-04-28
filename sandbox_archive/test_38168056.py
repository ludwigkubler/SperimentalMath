# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product, combinations

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

class MetricGadget:
    def __init__(self, X, Y, g):
        self.X = X
        self.Y = Y
        self.g = g

    def distance(self, x1, x2):
        return hamming_distance(x1, x2)

def generate_truth_table(f, domain):
    return {x: f(x) for x in domain}

def partition_space(space, num_partitions):
    partitions = []
    n = len(space)
    step = n // num_partitions
    for i in range(num_partitions):
        start = i * step
        end = (i + 1) * step if i < num_partitions - 1 else n
        partitions.append(space[start:end])
    return partitions

def find_min_cost_protocol(truth_table, max_depth=100):
    def dfs(node, depth):
        if depth == max_depth:
            return float('inf'), []
        min_cost = float('inf')
        best_partition = None
        for partition in partitions:
            cost = 0
            for x in node:
                y = truth_table[x]
                if not any(hamming_distance(x, p) < radius for p in partition):
                    cost += 1
            if cost < min_cost:
                min_cost = cost
                best_partition = partition
        return min_cost, [best_partition]

    partitions = partition_space(list(truth_table.keys()), 2)
    return dfs({}, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    b = random.choice([2, 3, 4])
    n = random.choice([2, 3, 4])

    X = list(product(range(2), repeat=b)) + list(range(b))
    Y = range(b)
    g = lambda x, y: x[y]
    G = MetricGadget(X, Y, g)

    def AND(x):
        return all(xi == 1 for xi in x)

    def OR(x):
        return any(xi == 1 for xi in x)

    def PARITY(x):
        return sum(xi for xi in x) % 2

    def Tribes(k, n):
        if len(x) != k * n:
            raise ValueError("Input length must be k*n")
        return all(sum(x[i:i+n]) % 2 == 1 for i in range(0, len(x), n))

    functions = [AND, OR, PARITY]
    if random.random() < 0.5:
        functions.append(lambda x: Tribes(2, 2)(x))

    results = []
    for f in functions:
        truth_table = generate_truth_table(f, X)
        protocol_cost, _ = find_min_cost_protocol(truth_table)
        R = max(hamming_distance(x, y) for x in X for y in Y)
        m_Pi = 2 ** protocol_cost / (b * n)
        CC_f_Gn = protocol_cost
        Q_f = len(truth_table)
        if CC_f_Gn >= Q_f - 2 * math.log2(b * n):
            results.append((True, ""))
        else:
            results.append((False, f"CC(f∘G^n)={CC_f_Gn} < {Q_f} - 2*log2({b}*{n})"))

    conjecture_holds = all(result[0] for result in results)
    counterexample = "; ".join(result[1] for result in results if not result[0])
    return {
        "metric_name": "CC(f∘G^n)",
        "metric_value": sum(CC_f_Gn for CC_f_Gn, _ in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) if x else 11 for x in input().split()]
    if not seeds:
        seeds = [11, 23, 37, 53, 71]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")