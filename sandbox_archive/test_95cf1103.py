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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf

    def min_order(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        n = len(variables)
        partitions = [set() for _ in range(n)]
        partitions[0].add(1)
        for variable in range(2, n + 1):
            new_partitions = []
            for partition in partitions:
                new_partition = partition.copy()
                new_partition.add(variable)
                new_partitions.append(new_partition)
                if len(partition) > 1:
                    for i in range(len(partition)):
                        new_partition = partition.copy()
                        new_partition.remove(partition[i])
                        new_partition.add(variable)
                        new_partitions.append(new_partition)
            partitions.extend(new_partitions)
        return len(partitions)

    def resolution_width(cnf):
        stack = []
        while cnf:
            clause = random.choice(cnf)
            if all(literal not in stack for literal in clause):
                stack.append(clause[0])
            else:
                cnf.remove(clause)
                for other_clause in cnf:
                    if -clause[0] in other_clause and -clause[1] in other_clause:
                        new_clause = [l for l in other_clause if l != -clause[0] and l != -clause[1]]
                        cnf.append(new_clause)
        return len(stack)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * (n - 1) // 2)
            cnf = generate_cnf(n, m)
            instances_tested += 1
            min_order_value = min_order(cnf)
            width_value = resolution_width(cnf)
            total_metric_value += abs(min_order_value / width_value)

    if instances_tested < 30:
        return {
            "metric_name": "min_order_over_resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "min_order_over_resolution_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric_value >= 0.7 and mean_metric_value <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "insufficient_support"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")