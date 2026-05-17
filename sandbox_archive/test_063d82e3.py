# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def cycle_type(perm):
    cycles = []
    visited = set()
    for i in range(len(perm)):
        if i not in visited:
            cycle = []
            j = i
            while j not in visited:
                visited.add(j)
                cycle.append(j)
                j = perm[j]
            cycles.append(tuple(cycle))
    return tuple(sorted(cycles, key=lambda x: (len(x), x)))

def murnaghan_nakayama(n):
    if n == 0:
        return {(): 1}
    if n == 1:
        return {(1,): 1}
    prev = murnaghan_nakayama(n - 1)
    current = defaultdict(int)
    for partition, value in prev.items():
        for i in range(len(partition)):
            new_partition = list(partition)
            new_partition[i] += 1
            new_partition = tuple(sorted(new_partition, reverse=True))
            current[new_partition] += value
        new_partition = list(partition) + [1]
        new_partition = tuple(sorted(new_partition, reverse=True))
        current[new_partition] -= value
    return current

def immanant(M, chi_lambda):
    n = len(M)
    total = 0
    for perm in itertools.permutations(range(n)):
        ct = cycle_type(perm)
        if ct in chi_lambda:
            term = chi_lambda[ct]
            for i in range(n):
                term *= M[i][perm[i]]
            total += term
    return total

def compute_variance(M, chi_tables):
    n = len(M)
    immanants = []
    for chi_lambda in chi_tables.values():
        I_lambda = immanant(M, chi_lambda)
        if I_lambda != 0:
            immanants.append(math.log2(1 + abs(I_lambda)))
    if not immanants:
        return 0.0
    mean = sum(immanants) / len(immanants)
    variance = sum((x - mean) ** 2 for x in immanants) / len(immanants)
    return variance

def run_trial(seed):
    random.seed(seed)
    n_values = [5, 6, 7]
    chi_tables = {n: murnaghan_nakayama(n) for n in n_values}

    results = []
    for n in n_values:
        # Uniform random matrix
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        V_uniform = compute_variance(M, chi_tables[n])

        # Padded matrix
        m = n // 2
        M_prime = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
        J = [[1 for _ in range(n - m)] for _ in range(n - m)]
        M_pad = [row + [0] * (n - m) for row in M_prime] + [[0] * m + row for row in J]
        V_pad = compute_variance(M_pad, chi_tables[n])

        results.append({
            "n": n,
            "V_uniform": V_uniform,
            "V_pad": V_pad,
            "ratio": V_uniform / V_pad if V_pad != 0 else float('inf')
        })

    metric_value = sum(r["ratio"] for r in results) / len(results)
    conjecture_holds = all(r["ratio"] >= 4 for r in results)
    counterexample = "" if conjecture_holds else f"n={n} seed={seed} V_uniform={V_uniform} V_pad={V_pad}"

    return {
        "metric_name": "V_uniform / V_pad ratio",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)

    if all(t["conjecture_holds"] for t in trials) and mean_metric >= 4:
        print(f"RESULT: SUPPORTED mean={mean_metric:.2f} std={std_metric:.2f} support_fraction={support_fraction:.2f}")
    elif any(not t["conjecture_holds"] for t in trials):
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")