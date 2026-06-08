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
        n = len(A)
        for i in range(n):
            max_row = i + random.randint(0, n - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        Lrank_sum = 0
        VarianceRank_sum = 0
        for _ in range(5):  # Sample 5 random instances per size
            M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            rank = gaussian_elimination(M)
            Lrank = rank  # Placeholder for actual L-function rank computation
            VarianceRank = variance([sum(row) for row in M])
            instances_tested += 1
            Lrank_sum += Lrank
            VarianceRank_sum += VarianceRank
        
        if instances_tested < 5:
            continue
        
        mean_Lrank = Lrank_sum / instances_tested
        mean_VarianceRank = VarianceRank_sum / instances_tested
        correlation_coefficient = (instances_tested * sum(Lrank * VarianceRank for Lrank, VarianceRank in zip(results, results)) - 
                                   mean_Lrank * mean_VarianceRank) / math.sqrt((instances_tested * sum(Lrank ** 2 for Lrank in results) - mean_Lrank ** 2) *
                                                                 (instances_tested * sum(VarianceRank ** 2 for VarianceRank in results) - mean_VarianceRank ** 2))
        
        if correlation_coefficient > 0.7:
            conjecture_holds = True
        else:
            conjecture_holds = False
        
        results.append(correlation_coefficient)
    
    metric_name = "Correlation Coefficient"
    metric_value = sum(results) / len(results)
    n_max = max(n_values)
    counterexample = "" if all(correlation >= 0.7 for correlation in results) else "correlation_below_threshold"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested * len(n_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result >= 0.7) / len(results)
    
    if all(result >= 0.7 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result < 0.7 for result in results):
        first_failing_seed = seeds[results.index(next(x for x in results if x < 0.7))]
        print(f"RESULT: FALSIFIED counterexample='correlation_below_threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")