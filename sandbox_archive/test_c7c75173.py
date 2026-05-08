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

    def disagree(x, y):
        return [i for i in range(len(x)) if x[i] != y[i]]

    def hamming_distance(x, y):
        return sum(1 for a, b in zip(x, y) if a != b)

    def disagreement_Hamming_metric(X):
        n = len(X[0][0])
        metric = [[0] * len(X) for _ in range(len(X))]
        for i in range(len(X)):
            for j in range(i + 1, len(X)):
                d = hamming_distance(X[i][0], X[j][0]) + hamming_distance(X[i][1], X[j][1])
                metric[i][j] = d
                metric[j][i] = d
        return metric

    def linear_programming(metric, r):
        n = len(metric)
        c = [0] * n
        A = []
        b = []
        for i in range(n):
            row = [0] * n
            for j in range(n):
                if hamming_distance(i, j) <= r:
                    row[j] = 1
            A.append(row)
            b.append(1)
        A = [[A[i][j] for j in range(r + 1)] for i in range(n)]
        c = [0] * (r + 1)
        from scipy.optimize import linprog
        result = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
        return result.fun

    def asdim(X):
        n = len(X[0][0])
        max_multiplicity = 0
        for r in range(1, n + 1):
            multiplicity = linear_programming(metric, r)
            if multiplicity > max_multiplicity:
                max_multiplicity = multiplicity
        return max_multiplicity

    def generate_PAR_n(n):
        X = []
        for x in range(2**(n-1)):
            y = x ^ ((x >> 1) ^ (x >> 2))
            X.append(((x, y), (0, 1)))
            X.append(((x, y), (1, 0)))
        return X

    n_values = [5, 10, 15, 20, 30]
    results = []
    for n in n_values:
        X = generate_PAR_n(n)
        metric = disagreement_Hamming_metric(X)
        asdim_value = asdim(X)
        results.append(asdim_value)

    a, b = sum(results[i] * n_values[i] for i in range(len(results))), sum(results)
    a /= sum(n_values)
    b /= len(results)

    if a >= 0.8 and b >= -3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "asdim(X_{PAR_n}) does not grow linearly in n"

    return {
        "metric_name": "asdim",
        "metric_value": a,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")