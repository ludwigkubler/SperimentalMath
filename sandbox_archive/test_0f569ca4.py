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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def truth_table_from_cnf(cnf):
        n = max(abs(lit) for lit in cnf)
        truth_table = []
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            row = [1 if any((lit > 0 and assignment[abs(lit)-1]) or (lit < 0 and not assignment[abs(lit)-1]) for lit in clause) else 0 for clause in cnf]
            truth_table.append(row)
        return truth_table
    
    def frobenius_class(truth_table):
        n = len(truth_table[0])
        primes = set()
        for i in range(n):
            for j in range(i+1, n):
                if all(truth_table[row][i] == truth_table[row][j] for row in range(len(truth_table))):
                    primes.add(abs(j-i))
        return len(primes)
    
    def communication_complexity_rank_variance(truth_table):
        n = len(truth_table[0])
        rank_variances = []
        for i in range(n):
            for j in range(i+1, n):
                row_i = truth_table[i]
                row_j = truth_table[j]
                diff_count = sum(1 for x, y in zip(row_i, row_j) if x != y)
                rank_variances.append(diff_count / n)
        return math.variance(rank_variances)
    
    def linear_function(n):
        return 2 * n
    
    cnf = generate_cnf(5)
    truth_table = truth_table_from_cnf(cnf)
    frobenius_class_size = frobenius_class(truth_table)
    rank_variance = communication_complexity_rank_variance(truth_table)
    C_n = linear_function(len(cnf))
    
    metric_value = abs(frobenius_class_size - C_n * rank_variance)
    instances_tested = 1
    n_max = len(cnf)
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Frobenius Class Size and Communication Complexity Rank Variance",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")