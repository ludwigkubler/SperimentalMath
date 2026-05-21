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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_mult(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                result[i][j] = sum(A[i][l] * B[l][j] for l in range(len(B)))
        return result

    def generate_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        clique_edges = random.sample(edges, k)
        dnf = []
        for edge in clique_edges:
            term = [0] * (n * (n - 1) // 2)
            idx = edge[0] * (n - edge[0]) // 2 + edge[1]
            term[idx] = 1
            dnf.append(term)
        return dnf

    def generate_random_dnf(n, m):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        dnf = []
        for _ in range(m):
            term_width = random.randint(2, n-1)
            term_edges = random.sample(edges, term_width)
            term = [0] * (n * (n - 1) // 2)
            for edge in term_edges:
                idx = edge[0] * (n - edge[0]) // 2 + edge[1]
                term[idx] = 1
            dnf.append(term)
        return dnf

    def certifier(dnf, x):
        live_terms = [i for i, term in enumerate(dnf) if any(x[j] == 1 for j in range(len(term)))]
        while True:
            if not live_terms:
                break
            max_live_term = max(live_terms, key=lambda i: sum(1 for j in range(len(dnf[i])) if dnf[i][j] * x[j] > 0))
            live_terms.remove(max_live_term)
            for j in range(len(dnf[max_live_term])):
                if dnf[max_live_term][j] * x[j] > 0:
                    x[j] = 1
        return sum(1 for term in dnf if all(x[j] == term[j] for j in range(len(term))))

    def calculate_mu(dnf, n):
        k = math.ceil(math.sqrt(n))
        D_k = [random.getrandbits(k) for _ in range(n)]
        mu = 0
        for x in D_k:
            x = [int(bit) for bit in bin(x)[2:].zfill(n)]
            mu += certifier(dnf, x)
        return mu / len(D_k)

    n_values = [6, 7, 8, 9, 10]
    k_values = [3, 4]
    m_values = [10, 30, n**2]

    results = []
    for n in n_values:
        for k in k_values:
            F_clique = generate_k_clique_dnf(n, k)
            mu_clique = calculate_mu(F_clique, n)
            results.append({"n": n, "k": k, "F_type": "clique", "mu": mu_clique})

            for m in m_values:
                F_rand = generate_random_dnf(n, m)
                mu_rand = calculate_mu(F_rand, n)
                results.append({"n": n, "k": k, "F_type": "random", "m": m, "mu": mu_rand})

    mean_mu_clique = sum(result["mu"] for result in results if result["F_type"] == "clique") / len(results)
    std_mu_clique = math.sqrt(sum((result["mu"] - mean_mu_clique) ** 2 for result in results if result["F_type"] == "clique") / len(results))
    support_fraction_clique = sum(1 for result in results if result["F_type"] == "clique" and result["mu"] <= 3 * math.log2(result["n"]) + 8) / len(results)
    
    mean_mu_rand = sum(result["mu"] for result in results if result["F_type"] == "random") / len(results)
    std_mu_rand = math.sqrt(sum((result["mu"] - mean_mu_rand) ** 2 for result in results if result["F_type"] == "random") / len(results))
    support_fraction_rand = sum(1 for result in results if result["F_type"] == "random" and result["m"] == n**2 and result["mu"] <= 3 * math.log2(result["n"]) + 8) / len(results)

    if mean_mu_clique > mean_mu_rand:
        support_fraction = support_fraction_clique
    else:
        support_fraction = support_fraction_rand

    if support_fraction >= 0.95 and mean_mu_clique / mean_mu_rand > 1:
        return {
            "metric_name": "mu_ratio",
            "metric_value": mean_mu_clique / mean_mu_rand,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for result in results:
            if result["F_type"] == "clique" and result["mu"] > 3 * math.log2(result["n"]) + 8:
                return {
                    "metric_name": "mu_clique",
                    "metric_value": result["mu"],
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"n={result['n']}, k={result['k']}"
                }
            elif result["F_type"] == "random" and result["m"] == n**2 and result["mu"] > 3 * math.log2(result["n"]) + 8:
                return {
                    "metric_name": "mu_rand",
                    "metric_value": result["mu"],
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"n={result['n']}, k={result['k']}, m={result['m']}"
                }
        return {
            "metric_name": "support_fraction",
            "metric_value": support_fraction,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_mu_ratio = sum(r["metric_value"] for r in results if "mu_ratio" in r) / len(results)
    std_mu_ratio = math.sqrt(sum((r["metric_value"] - mean_mu_ratio) ** 2 for r in results if "mu_ratio" in r) / len(results))
    support_fraction = sum(1 for r in results if "support_fraction" not in r and r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_mu_ratio} std={std_mu_ratio} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] == False for r in results):
        for r in results:
            if "counterexample" in r and r["conjecture_holds"] == False:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")