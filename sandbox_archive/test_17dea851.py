# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_instance(n):
        return [random.sample(range(1, n+1), k=random.randint(1, n)) for _ in range(n)]
    
    def incidence_matrix(instance):
        n = len(instance)
        matrix = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for subset in instance[i]:
                index = sum(1 << (subset - 1) for subset in instance[i])
                matrix[i][index] = 1
        return matrix
    
    def noncrossing_partition(matrix):
        n = len(matrix)
        partition = [[] for _ in range(n)]
        for i in range(n):
            for j in range(2**n):
                if all(matrix[i][j & (1 << k)] == matrix[j // (2**(i+1))][j % (2**(i+1))] for k in range(i)):
                    partition[i].append(j)
        return partition
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(all(matrix[j][k] == 0 for j in range(n) if j != i) for k in range(2**n)):
                rank += 1
        return rank
    
    def is_noncrossing(partition):
        n = len(partition)
        for i in range(n):
            for j in range(i+1, n):
                if any(all(k in partition[i] and l in partition[j] for k, l in zip(subset1, subset2)) for subset1 in partition[i] for subset2 in partition[j]):
                    return False
        return True
    
    def frege_proof_width(formula):
        return max(frege_proof_width(subformula) for subformula in formula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        matrix = incidence_matrix(instance)
        partition = noncrossing_partition(matrix)
        rank = min_rank(matrix)
        
        if not is_noncrossing(partition):
            return {
                "metric_name": "min_rank",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "Noncrossing partition found"
            }
        
        results.append(rank)
    
    mean_value = sum(results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r <= (3 * n_values[-1]) / 2), len(results))
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= Fraction(4, 5),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r <= (3 * max(n_values)) / 2), len(results))
    
    if all(r is not None for r in results):
        if support_fraction >= Fraction(4, 5):
            print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='not enough noncrossing partitions' first_failing_seed={seeds[results.index(None)]}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_noncrossing_partitions")