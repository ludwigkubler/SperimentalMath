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
    
    def and_or_tree(n):
        if n == 1:
            return random.choice([True, False])
        else:
            left = and_or_tree(n // 2)
            right = and_or_tree(n - n // 2)
            return random.choice([left and right, left or right])
    
    def communication_complexity(tree):
        if isinstance(tree, bool):
            return 0
        else:
            return 1 + max(communication_complexity(tree[0]), communication_complexity(tree[1]))
    
    def geometric_quantization_space(tree):
        if isinstance(tree, bool):
            return [[1], [0]]
        else:
            left = geometric_quantization_space(tree[0])
            right = geometric_quantization_space(tree[1])
            result = []
            for l in left:
                for r in right:
                    result.append([l[0] * r[0], l[0] * r[1], l[1] * r[0], l[1] * r[1]])
            return result
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
                break
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for j in range(m):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    n = random.randint(5, 40)
    tree = and_or_tree(n)
    comm_complexity = communication_complexity(tree)
    
    if comm_complexity != n:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Communication complexity is {comm_complexity}, not O(n)"
        }
    
    q_space = geometric_quantization_space(tree)
    rank_q_space = rank(q_space)
    
    c = 0.5
    if rank_q_space >= c * math.log2(n):
        return {
            "metric_name": "rank",
            "metric_value": rank_q_space,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank_q_space,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank_q_space} < {c * math.log2(n)}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")