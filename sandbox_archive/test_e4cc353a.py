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
    
    n = random.randint(5, 40)
    protocol = [random.choice([0, 1]) for _ in range(n)]
    
    # Define a simple mapping from protocol to group elements
    group_elements = {i: (i % 2, i // 2) for i in range(n)}
    R = [[group_elements[protocol[i]] if protocol[i] == protocol[j] else (0, 0) for j in range(n)] for i in range(n)]
    
    # Calculate the minimal rank of the matrix representation
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            factor = 1 / matrix[i][i]
            for j in range(n):
                matrix[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    τ_R = gaussian_elimination(R)
    
    # Check the conjecture
    expected_rank = n**2 * math.log(n, 2)
    margin = expected_rank * 0.05
    conjecture_holds = τ_R >= expected_rank - margin and τ_R <= expected_rank + margin
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": τ_R,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"rank={τ_R}, expected={expected_rank}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")