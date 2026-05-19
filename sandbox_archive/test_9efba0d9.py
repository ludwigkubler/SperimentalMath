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

# Define permutations as tuples
a = (1, 2, 3, 4, 5)
b = (1, 3, 5, 2, 4)

def inverse(p):
    return tuple(p.index(i + 1) + 1 for i in range(5))

def compose(p1, p2):
    return tuple(p1[p2[i] - 1] for i in range(5))

def perm_matrix(p):
    M = [[0] * 5 for _ in range(5)]
    for i in range(5):
        M[p[i] - 1][i] = 1
    return M

def frobenius_norm(M, N):
    sum_sq = 0
    for i in range(5):
        for j in range(5):
            sum_sq += (M[i][j] - N[i][j]) ** 2
    return math.sqrt(sum_sq)

def barrington_and(n):
    if n == 2:
        return [(1, a, b), (2, b, a)]
    else:
        and_n_2 = barrington_and(n // 2)
        new_program = []
        for step in and_n_2:
            literal_index, perm_for_x0, perm_for_x1 = step
            new_program.append((literal_index * 4 + 1, compose(a, perm_for_x0), compose(b, perm_for_x1)))
            new_program.append((literal_index * 4 + 2, compose(a, perm_for_x1), compose(b, perm_for_x0)))
        return new_program

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 16, 32]
    results = []
    
    for n in n_values:
        program = barrington_and(n)
        L_n = n ** 2
        M_bar = [[0] * 5 for _ in range(5)]
        
        for _ in range(30):
            x = tuple(random.randint(0, 1) for _ in range(n))
            π = [() for _ in range(L_n + 1)]
            π[0] = ()
            
            for i in range(1, L_n + 1):
                literal_index, perm_for_x0, perm_for_x1 = program[i - 1]
                if x[literal_index - 1] == 0:
                    π[i] = compose(perm_for_x0, π[i - 1])
                else:
                    π[i] = compose(perm_for_x1, π[i - 1])
            
            M_bar = [[M_bar[i][j] + perm_matrix(π[i])[i][j] for j in range(5)] for i in range(5)]
        
        M_bar = [[entry / L_n for entry in row] for row in M_bar]
        J = [[Fraction(1, 5) if i == j else Fraction(0) for j in range(5)] for i in range(5)]
        frobenius_defect = frobenius_norm(M_bar, J)
        
        results.append(frobenius_defect)
    
    D_bar_n_values = [results[i] / results[i - 1] for i in range(1, len(results))]
    slopes = [math.log2(D_bar_n_values[i]) for i in range(len(D_bar_n_values))]
    
    conjecture_holds = all(slope > 0.5 and slope < 3.0 for slope in slopes)
    counterexample = "" if conjecture_holds else "slope_outside_band"
    
    return {
        "metric_name": "Frobenius Fourier Defect",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values) * 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
    results = [run_trial(seed)["metric_value"] for seed in seeds]
    support_fraction = sum(run_trial(seed)["conjecture_holds"] for seed in seeds) / len(seeds)
    
    if all(trial["conjecture_holds"] for trial in run_trials):
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results):.4f} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results)/len(results)):.4f} support_fraction={support_fraction:.2f}")
    elif any(not trial["conjecture_holds"] for trial in run_trials):
        first_failing_seed = next(seed for seed, trial in enumerate(run_trials) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_outside_band\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")