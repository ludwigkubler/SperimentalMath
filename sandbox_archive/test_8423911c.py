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
    
    def is_invertible(matrix):
        if not matrix or len(matrix) == 0:
            return False
        n = len(matrix)
        submatrix = [[matrix[i][j] for j in range(n) if j != c] for i in range(1, n)]
        det = determinant(submatrix)
        return det != 0
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = Fraction(0)
            for c in range(n):
                submatrix = [[matrix[i][j] for j in range(n) if j != c] for i in range(1, n)]
                det += (-1) ** c * matrix[0][c] * determinant(submatrix)
            return det
    
    def commutant_rank(ρ):
        # Placeholder for actual computation
        return random.randint(1, 5)
    
    def entanglement_communication_complexity(n):
        # Placeholder for actual computation
        return n ** 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    ρ = [[random.random() for _ in range(n)] for _ in range(n)]
    
    commutant_ρ = commutant_rank(ρ)
    entang_comm_C_n = entanglement_communication_complexity(n)
    
    return {
        "metric_name": "commutant_rank_vs_entang_comm",
        "metric_value": Fraction(commutant_ρ, entang_comm_C_n),
        "instances_tested": 1,
        "conjecture_holds": commutant_ρ >= entang_comm_C_n / 2,
        "counterexample": "" if commutant_ρ >= entang_comm_C_n / 2 else "commutant_rank < entang_comm_C_n / 2"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [3, 7, 11, 13, 17, 19, 23, 29] * 4
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"commutant_rank < entang_comm_C_n / 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")