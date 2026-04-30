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
    n = 40
    ε = 1e-3
    
    def tensor_product(A, B):
        result = []
        for a_row in A:
            new_row = []
            for b_col in zip(*B):
                new_row.append([a * b for a, b in zip(a_row, b_col)])
            result.extend(new_row)
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def free_entropy(M):
        det = determinant([[M[i][j] + ε for j in range(len(M))] for i in range(len(M))])
        if det <= 0:
            return float('-inf')
        return (1 / n) * math.log(det)
    
    random.seed(seed)
    M_P = [[0] * (2 ** n) for _ in range(2 ** n)]
    local_matrices = [random.choice([[Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), -Fraction(1, 2)]]) for _ in range(n)]
    
    for i in range(n):
        M_P = tensor_product(M_P, local_matrices[i])
    
    ϕ_M_P = free_entropy(M_P)
    
    return {
        "metric_name": "free entropy",
        "metric_value": ϕ_M_P,
        "instances_tested": 1,
        "conjecture_holds": ϕ_M_P <= math.log(n),
        "counterexample": "" if ϕ_M_P <= math.log(n) else "IP_2 trivial BP"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 trivial BP\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")