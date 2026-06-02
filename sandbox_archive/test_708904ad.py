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

# Helper functions
def log2(x):
    return math.log2(x) if x > 0 else -math.inf

def entropy(probs):
    return sum(p * log2(p) for p in probs if p > 0)

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        if M[i][i] == 0:
            raise ValueError("Singular matrix")
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters
    n_values = [5, 10, 15, 20, 30, 40]
    instances_per_n = 30
    total_instances = sum(instances_per_n for n in n_values)
    
    mli_sum = 0
    log_ent_sum = 0
    instances_tested = 0
    n_max = 1
    
    # Generate random CNFs and compute mli and ent
    for n in n_values:
        for _ in range(instances_per_n):
            clauses = []
            for _ in range(random.randint(1, n * (n + 1) // 2)):
                clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
                if all(clause[i] != -clauses[j][i] for j in range(len(clauses))):
                    clauses.append(clause)
            mli = len(clauses) / (n * (n + 1) // 2)
            ent = entropy([len(clause) / n for clause in clauses])
            mli_sum += mli
            log_ent_sum += log2(ent)
            instances_tested += 1
            n_max = max(n_max, n)
    
    # Compute correlation and mean absolute difference
    if instances_tested == total_instances:
        avg_mli = mli_sum / instances_tested
        avg_log_ent = log_ent_sum / instances_tested
        correlation = (mli_sum * log_ent_sum - instances_tested * avg_mli * avg_log_ent) / (
            math.sqrt(mli_sum**2 - instances_tested * avg_mli**2) *
            math.sqrt(log_ent_sum**2 - instances_tested * avg_log_ent**2)
        )
        mean_abs_diff = abs(avg_mli - avg_log_ent)
        
        # Check acceptance criterion
        if correlation >= 0.8 and mean_abs_diff <= 3:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "correlation_threshold_not_met"
    else:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    return {
        "metric_name": "mli_vs_log_ent",
        "metric_value": avg_mli,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and std of metric_value
    if all("metric_value" in r for r in results):
        values = [r["metric_value"] for r in results]
        mean_value = sum(values) / len(values)
        std_value = math.sqrt(sum((v - mean_value)**2 for v in values) / len(values))
        
        # Compute fraction of seeds where conjecture_holds
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(r["counterexample"] == "correlation_threshold_not_met" for r in results):
            print("RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed=1")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE missing_metric_value")