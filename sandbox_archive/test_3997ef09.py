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
    
    def generate_random_bipartite_state(n):
        state = [[random.random() for _ in range(n)] for _ in range(n)]
        return state
    
    def matrix_multiplication(A, B):
        result = []
        for i in range(len(A)):
            row = []
            for j in range(len(B[0])):
                sum_product = 0
                for k in range(len(B)):
                    sum_product += A[i][k] * B[k][j]
                row.append(sum_product)
            result.append(row)
        return result
    
    def communication_complexity(state):
        n = len(state)
        total_bits = 0
        for i in range(n):
            for j in range(n):
                if state[i][j] != 0:
                    total_bits += math.log2(abs(state[i][j]))
        return total_bits
    
    def minimal_local_index_of_topological_entanglement_rank(state):
        n = len(state)
        ranks = [sum(row) for row in state]
        mter = max(ranks)
        return mter
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mter = 0
    total_cc = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            state = generate_random_bipartite_state(n)
            mter = minimal_local_index_of_topological_entanglement_rank(state)
            cc = communication_complexity(state)
            instances_tested += 1
            total_mter += mter
            total_cc += cc
    
    mean_mter = total_mter / instances_tested
    mean_cc = total_cc / instances_tested
    correlation_coefficient = (instances_tested * sum(mter * cc for mter, cc in zip(total_mter, total_cc)) -
                               total_mter * total_cc) / math.sqrt(instances_tested * sum(mter**2 for mter in total_mter) - total_mter**2 *
                                                                 instances_tested * sum(cc**2 for cc in total_cc) - total_cc**2)
    
    conjecture_holds = correlation_coefficient >= 0.9
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")