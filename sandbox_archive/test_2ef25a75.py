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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def xor_circuit(n, depth):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            inputs = [xor_circuit(n-1, depth-1) for _ in range(2)]
            return [inputs[0][i] ^ inputs[1][i] for i in range(len(inputs[0]))]
    
    def cycle_space(circuit):
        n = len(circuit)
        V = [tuple(circuit[i:i+n]) for i in range(len(circuit) - n + 1)]
        E = []
        for u in range(len(V)):
            for v in range(u+1, len(V)):
                if sum(1 for i in range(n) if V[u][i] != V[v][i]) == 1:
                    E.append((u, v))
        return V, E
    
    def poincare_dual_complex(V, E):
        n = len(V[0])
        dual_cells = {}
        for d in range(n+1):
            dual_cells[d] = []
        for u, v in E:
            if abs(u - v) == 1:
                dual_cells[1].append((u, v))
            elif abs(u - v) == n-1:
                dual_cells[n-2].append((u, v))
        return dual_cells
    
    def minimal_index(dual_cells):
        indices = []
        for d in range(1, len(dual_cells)):
            if dual_cells[d]:
                indices.append(len(dual_cells[d]))
        if not indices:
            return 0
        return min(indices)
    
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            depth = random.randint(1, min(n, 40))
            circuit = xor_circuit(n, depth)
            V, E = cycle_space(circuit)
            K_C = poincare_dual_complex(V, E)
            mu_K_C = minimal_index(K_C)
            metric_value += mu_K_C
            instances_tested += 1
    
    conjecture_holds = True
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            depth = random.randint(1, min(n, 40))
            circuit = xor_circuit(n, depth)
            V, E = cycle_space(circuit)
            K_C = poincare_dual_complex(V, E)
            mu_K_C = minimal_index(K_C)
            if mu_K_C > (depth ** n * math.log(n)) * 2:
                conjecture_holds = False
                counterexample = f"n={n}, depth={depth}, mu(K_C)={mu_K_C}"
                break
    
    return {
        "metric_name": "minimal_index",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")