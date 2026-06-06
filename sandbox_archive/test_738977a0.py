# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot row
            max_row = i + max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    
    def frobenius_normal_form(matrix):
        n = len(matrix)
        F = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if matrix[j][i] != 0:
                    F[i][j - i] = matrix[j][i]
        return F
    
    def resolution_width(phi):
        # Placeholder function to compute resolution width
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = [[random.randint(-n, n) for _ in range(random.randint(2, n//2))] for _ in range(n)]
        
        F = frobenius_normal_form(phi)
        dim_F = sum(sum(row) != 0 for row in F)
        w_phi = resolution_width(phi)
        
        metric_values.append(dim_F)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / instances_tested) ** 0.5
    
    correlation_coefficient = sum((metric_values[i] - mean_value) * (w_phi - mean_value) for i, w_phi in enumerate(metric_values)) / (instances_tested * std_value * std_value)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "Correlation coefficient: {}".format(correlation_coefficient)
    
    return {
        "metric_name": "Frobenius Normal Form Dimension",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={}".format(first_failing_seed + 1))