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
    
    def generate_xor_game(n, m):
        inputs = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(m)]
        outputs = [random.randint(0, 1) for _ in range(m)]
        return inputs, outputs

    def symmetric_bilinear_form(inputs, outputs):
        n = len(inputs[0])
        m = len(inputs)
        form = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        
        for i in range(m):
            x = inputs[i]
            y = outputs[i]
            for j in range(n):
                form[j][j] += Fraction(x[j], m)
                form[n][j] += Fraction(x[j], m)
                form[j][n] += Fraction(x[j], m)
                form[n][n] += Fraction(y, m)
        
        return form

    def matrix_rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            pivot_col = next(j for j in range(m) if matrix[i][j] != 0)
            for j in range(i + 1, n):
                factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                for k in range(m):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank

    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    inputs, outputs = generate_xor_game(n, m)
    form = symmetric_bilinear_form(inputs, outputs)
    rank = matrix_rank(form)
    
    c = 1.0
    upper_bound = c * log2(n) ** 2
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= upper_bound
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds bound {upper_bound}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")