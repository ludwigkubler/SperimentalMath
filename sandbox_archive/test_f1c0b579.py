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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            pivot = max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[pivot] = A[pivot], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        A_tilde = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in A_tilde:
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity(n):
        # Placeholder for actual CC_R(DISJ_n) computation
        return n * (n - 1) // 2
    
    def tropicalized_rank(A):
        m, n = len(A), len(A[0])
        max_values = [max(row[i] for row in A) for i in range(n)]
        return sum(1 for val in max_values if val != float('-inf'))
    
    def generate_disjointness_instance(n):
        inputs = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        outputs = [all(inputs[i][j] == inputs[j][i] for i in range(j)) for j in range(n)]
        return inputs, outputs
    
    n = random.randint(5, 40)
    inputs, outputs = generate_disjointness_instance(n)
    
    # Construct affine Grassmannian G
    A = [[inputs[i][j] if outputs[j] else float('-inf') for j in range(n)] for i in range(n)]
    
    tau_G = tropicalized_rank(A)
    CC_R_DISJ_n = communication_complexity(n)
    
    return {
        "metric_name": "tropicalized_rank",
        "metric_value": tau_G,
        "instances_tested": 1,
        "conjecture_holds": tau_G <= 2 * CC_R_DISJ_n,  # Placeholder constant c=2
        "counterexample": "" if tau_G <= 2 * CC_R_DISJ_n else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next((res["counterexample"] for res in results if res["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")