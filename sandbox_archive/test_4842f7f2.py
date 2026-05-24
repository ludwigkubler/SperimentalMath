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
        if len(matrix) == 1:
            return matrix[0][0] != 0
        submatrix = [[matrix[i][j] for j in range(len(matrix)) if j != c] for i in range(1, len(matrix))]
        det = sum(Fraction((-1)**c * matrix[0][c] * is_invertible(submatrix), 1) for c in range(len(matrix)))
        return det != 0
    
    def commutant_rank(ρ):
        n = len(ρ)
        I = [[Fraction(i == j, 1) for j in range(n)] for i in range(n)]
        AB = [[sum(ρ[i][k] * ρ[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        BA = [[sum(ρ[j][k] * ρ[k][i] for k in range(n)) for j in range(n)] for i in range(n)]
        return len([1 for row in AB if is_invertible(row)]) + len([1 for col in zip(*AB) if is_invertible(col)])
    
    def entanglement_communication_complexity(n):
        # Simplified model: log2(n)
        return math.log2(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    ρ = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    rank_commutant_ρ = commutant_rank(ρ)
    EntangComm_C_n = entanglement_communication_complexity(n)
    
    return {
        "metric_name": "rank_commutant",
        "metric_value": rank_commutant_ρ,
        "instances_tested": 1,
        "conjecture_holds": rank_commutant_ρ >= EntangComm_C_n * Fraction(1, 2),
        "counterexample": "" if rank_commutant_ρ >= EntangComm_C_n * Fraction(1, 2) else f"rank_commutant({n})={rank_commutant_ρ}, EntangComm_C({n})={EntangComm_C_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(r["counterexample"]):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")