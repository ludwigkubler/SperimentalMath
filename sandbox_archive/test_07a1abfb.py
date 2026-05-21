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
    
    def fourier_hat(f, U):
        return sum(f(x) * (-1)**(sum(U[i] for i in range(len(U)) if x & (1 << i))) / 2**len(f) for x in range(2**len(f)))
    
    def gram_matrix(f, d):
        B_d = [set(range(i+1)) for i in range(d+1)]
        Q_d = [[0] * len(B_d) for _ in range(len(B_d))]
        for S in B_d:
            for T in B_d:
                if len(S ^ T) <= d:
                    Q_d[B_d.index(S)][B_d.index(T)] = fourier_hat(f, S ^ T)
        return Q_d
    
    def negative_eigenvalue_gap(Q):
        eigenvalues = [eigval for eigval in math.eigvalsh(Q) if eigval < 0]
        return -min(eigenvalues) if eigenvalues else 0
    
    n_values = [6, 8, 10]
    results = []
    
    for n in n_values:
        # Sipser function
        S_n = lambda x: sum(1 if i % 2 == 0 else -1 for i in range(n)) & x
        Q_2_S_n = gram_matrix(S_n, 2)
        NG_2_S_n = negative_eigenvalue_gap(Q_2_S_n)
        
        # Random ACC0[3] circuits
        random.seed(seed)
        max_ng_2_circuit = 0
        for _ in range(30):
            circuit = [random.choice(['AND', 'OR', 'MOD3']) for _ in range(n * int(math.log2(n)))]
            Q_2_circuit = gram_matrix(circuit, 2)
            NG_2_circuit = negative_eigenvalue_gap(Q_2_circuit)
            max_ng_2_circuit = max(max_ng_2_circuit, NG_2_circuit)
        
        # Random truth tables
        random.seed(seed)
        max_ng_2_random = 0
        for _ in range(30):
            f = [random.choice([-1, 1]) for _ in range(2**n)]
            Q_2_random = gram_matrix(f, 2)
            NG_2_random = negative_eigenvalue_gap(Q_2_random)
            max_ng_2_random = max(max_ng_2_random, NG_2_random)
        
        results.append({
            "metric_name": "NG_2",
            "metric_value": NG_2_S_n,
            "instances_tested": 1,
            "conjecture_holds": NG_2_S_n >= Fraction(1, 8 * n) and NG_2_S_n - max_ng_2_circuit >= Fraction(1, 8 * n),
            "counterexample": "" if NG_2_S_n >= Fraction(1, 8 * n) and NG_2_S_n - max_ng_2_circuit >= Fraction(1, 8 * n) else f"Sipser function NG_2 = {NG_2_S_n}, max ACC0[3] NG_2 = {max_ng_2_circuit}"
        })
    
    return {
        "seed": seed,
        "metric_name": "NG_2",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else next(result["counterexample"] for result in results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
    
    NG_2_values = [result["metric_value"] for result in run_trials(seeds).values()]
    support_fraction = sum(result["conjecture_holds"] for result in run_trials(seeds).values()) / len(run_trials(seeds).values())
    
    if all(result["conjecture_holds"] for result in run_trials(seeds).values()):
        print(f"RESULT: SUPPORTED mean={sum(NG_2_values)/len(NG_2_values)} std=0 support_fraction=1")
    elif any(not result["conjecture_holds"] for result in run_trials(seeds).values()):
        first_failing_seed = next(seed for seed, result in run_trials(seeds).items() if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Sipser function NG_2 < 1/(8n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")