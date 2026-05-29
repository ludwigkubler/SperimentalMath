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
            random.shuffle(clause)
            cnf.append(clause)
        return cnf
    
    def resolution_length(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if -stack[i][0] in stack[j]:
                        new_clause = [x for x in stack[i] if x != -stack[j][0]] + [y for y in stack[j] if y != -stack[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    def formal_power_series_rank(cnf):
        m = len(cnf)
        n = max(abs(var) for clause in cnf for var in clause)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for var in clause:
                A[i][abs(var)] += 1 if var > 0 else -1
        rank = 0
        for row in A:
            if any(row[j] != 0 for j in range(n + 1)):
                rank += 1
                for i2, row2 in enumerate(A):
                    if i2 != i and any(row2[j] != 0 for j in range(n + 1)):
                        factor = Fraction(row2[i], row[i])
                        for j in range(n + 1):
                            row2[j] -= factor * row[j]
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    
    resolution_len = resolution_length(cnf)
    power_series_rank = formal_power_series_rank(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": Fraction(power_series_rank, resolution_len),
        "instances_tested": 1,
        "conjecture_holds": False if resolution_len == 0 else power_series_rank <= 2 * math.log(resolution_len, 2),
        "counterexample": "mapping_undefined" if resolution_len == 0 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result <= 2 * math.log(result, 2)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result > 2 * math.log(result, 2) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 2 * math.log(result, 2))
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")