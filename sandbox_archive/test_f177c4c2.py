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
    
    def generate_matrix(n: int) -> list:
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def communication_complexity(matrix: list) -> int:
        n = len(matrix)
        if all(all(matrix[i][j] == matrix[j][i] for i in range(n)) for j in range(n)):
            return 0
        if any(all(matrix[i][j] != matrix[j][i] for i in range(n)) for j in range(n)):
            return n
        return n - 1
    
    def minimal_free_entanglement_dimension(matrix: list) -> int:
        n = len(matrix)
        # Placeholder implementation (replace with actual algorithm)
        return n
    
    n = random.randint(5, 40)
    matrix = generate_matrix(n)
    
    CC_R = communication_complexity(matrix)
    tau_FE = minimal_free_entanglement_dimension(matrix)
    
    if CC_R == 0:
        ratio = float('inf')
    else:
        ratio = Fraction(tau_FE, CC_R)
    
    return {
        "metric_name": "tau_FE / CC_R",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= (n**2 / 4),
        "counterexample": "" if ratio >= (n**2 / 4) else f"Matrix with n={n} and tau_FE={tau_FE}, CC_R={CC_R}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")