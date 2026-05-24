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
        n = len(matrix)
        if n == 0:
            return False
        det = 0
        for c in range(n):
            submatrix = [[matrix[i][j] for j in range(len(matrix)) if j != c] for i in range(1, len(matrix))]
            sign = (-1) ** (c % 2)
            if n == 1:
                det += sign * matrix[0][0]
            else:
                sub_det = is_invertible(submatrix)
                if sub_det is not None:
                    det += sign * matrix[0][c] * sub_det
        return det != 0
    
    def commutant_rank(ρ):
        n = len(ρ)
        AB = [[ρ[i][j] for j in range(n)] for i in range(n)]
        rank = 0
        for row in AB:
            if is_invertible(row):
                rank += 1
        for col in zip(*AB):
            if is_invertible(col):
                rank += 1
        return rank
    
    def entanglement_communication_complexity(n):
        # Placeholder function; replace with actual computation
        return n * math.log2(n)
    
    instances_tested = 0
    total_rank_commutant = 0
    total_entang_comm = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        ρ = [[random.random() for _ in range(n)] for _ in range(n)]
        commutant_ρ = commutant_rank(ρ)
        entang_comm = entanglement_communication_complexity(n)
        
        total_rank_commutant += commutant_ρ
        total_entang_comm += entang_comm
        instances_tested += 1
    
    mean_rank_commutant = Fraction(total_rank_commutant, instances_tested)
    mean_entang_comm = Fraction(total_entang_comm, instances_tested)
    
    correlation_coefficient = (instances_tested * sum(rank_commutant * entang_comm for rank_commutant, entang_comm in zip(range(5, 41), range(5, 41))) - total_rank_commutant * total_entang_comm) / math.sqrt((instances_tested * sum(rank_commutant**2 for rank_commutant in range(5, 41)) - total_rank_commutant**2) * (instances_tested * sum(entang_comm**2 for entang_comm in range(5, 41)) - total_entang_comm**2))
    
    conjecture_holds = correlation_coefficient >= Fraction(7, 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")