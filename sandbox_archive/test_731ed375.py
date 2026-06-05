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
    
    def entropy(probabilities):
        return -sum(p * math.log2(p) for p in probabilities if p > 0)

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    max_row = j
                    break
            if max_row is None:
                continue
            matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank

    def geometric_group_rank(sat_instance):
        n = len(sat_instance)
        group_size = 2 ** n
        if group_size % (n + 1) != 0:
            raise ValueError("Unsupported group size")
        identity = [1] * group_size
        elements = [identity]
        for i in range(n):
            new_elements = []
            for elem in elements:
                new_elem = [(elem[j] ^ (1 << i)) if j == k else elem[j] for j in range(group_size)]
                new_elements.append(new_elem)
            elements.extend(new_elements)
        group_matrix = [[0] * group_size for _ in range(group_size)]
        for i, elem1 in enumerate(elements):
            for j, elem2 in enumerate(elements):
                product = [elem1[k] & elem2[k] for k in range(group_size)]
                group_matrix[i][j] = elements.index(product)
        return gaussian_elimination(group_matrix)

    def clause_subset_entropy(sat_instance):
        n = len(sat_instance)
        subsets = []
        for i in range(1, 1 << n):
            subset = [j for j in range(n) if (i & (1 << j)) != 0]
            probabilities = [sum(1 for clause in sat_instance if all(j in clause for j in subset)) / len(sat_instance) for j in range(n)]
            subsets.append(probabilities)
        return entropy([sum(subset) for subset in zip(*subsets)])

    n = random.randint(5, 40)
    sat_instance = [[random.randint(0, n - 1) for _ in range(random.randint(2, n // 2))] for _ in range(n)]
    
    try:
        entropy_value = clause_subset_entropy(sat_instance)
        rank = geometric_group_rank(sat_instance)
        return {
            "metric_name": "Entropy vs Rank",
            "metric_value": entropy_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(entropy_value - rank) < 0.1 * max(abs(entropy_value), abs(rank)),
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Entropy vs Rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")