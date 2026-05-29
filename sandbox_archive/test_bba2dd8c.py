# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def generate_clique_dnf(v, k):
    cliques = list(combinations(range(v), k))
    minterms = [frozenset(clique) for clique in cliques]
    return minterms

def count_edges(minterms):
    n = len(minterms)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if len(minterms[i] ^ minterms[j]) == 1:
                edges.append((i, j))
    return edges

def calculate_forman_ricci_curvature(edges, degrees):
    n_edges = len(edges)
    total_curvature = sum(4 - degrees[u] - degrees[v] for u, v in edges) / n_edges
    return total_curvature

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for v in [4, 10, 16, 20]:
        k = (v.bit_length() - 1).bit_length()
        minterms = generate_clique_dnf(v, k)
        edges = count_edges(minterms)
        
        degrees = {i: sum(1 for j in range(len(edges)) if i in edges[j]) for i in range(len(minterms))}
        forman_ricci_curvature = calculate_forman_ricci_curvature(edges, degrees)
        
        M_Fv = len(minterms)
        C_vk = v * (v - 1) // 2
        
        metric_value = forman_ricci_curvature
        conjecture_holds = M_Fv == C_vk and abs(forman_ricci_curvature - (4 - 2 * k * (v - k))) <= 1
        counterexample = "" if conjecture_holds else f"M(F*_v)={M_Fv}, C(v,k)={C_vk}, forman_ricci_curvature={forman_ricci_curvature}"
        
        results.append({
            "metric_name": "Forman-Ricci curvature",
            "metric_value": metric_value,
            "instances_tested": len(minterms),
            "n_max": v,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    all_results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.extend(trial_result["results"])
    
    M_Fv_values = [result["metric_value"] for result in all_results]
    conjecture_holds_fraction = sum(result["conjecture_holds"] for result in all_results) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={sum(M_Fv_values)/len(M_Fv_values):.2f} std={(sum((x - sum(M_Fv_values)/len(M_Fv_values))**2 for x in M_Fv_values) / len(M_Fv_values))**0.5:.2f} support_fraction=1.0")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(M_Fv_values)/len(M_Fv_values):.2f} std={(sum((x - sum(M_Fv_values)/len(M_Fv_values))**2 for x in M_Fv_values) / len(M_Fv_values))**0.5:.2f} support_fraction={conjecture_holds_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")