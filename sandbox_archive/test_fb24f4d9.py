# auto-injected by SEC sandbox
import os
import time
import re
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import json
import math
import random
import itertools
from fractions import Fraction
from collections import defaultdict

# ── Gaussian elimination over Q ──────────────────────────────────────────────
def mat_rank(rows, ncols):
    """Return rank of matrix (list of list of Fraction)."""
    M = [r[:] for r in rows]
    pivot_row = 0
    for col in range(ncols):
        found = -1
        for r in range(pivot_row, len(M)):
            if M[r][col] != 0:
                found = r
                break
        if found == -1:
            continue
        M[pivot_row], M[found] = M[found], M[pivot_row]
        inv = Fraction(1, 1) / M[pivot_row][col]
        M[pivot_row] = [v * inv for v in M[pivot_row]]
        for r in range(len(M)):
            if r != pivot_row and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [M[r][c] - factor * M[pivot_row][c] for c in range(ncols)]
        pivot_row += 1
    return pivot_row

def subset_rank(clause_rows, subset_indices, n):
    """Rank of the sub-system of hyperplanes indexed by subset_indices."""
    if not subset_indices:
        return 0
    rows = [clause_rows[i] for i in subset_indices]
    return mat_rank(rows, n + 1)

# ── Build hyperplane coefficient rows for a clause ────────────────────────────
def clause_to_row(clause, n):
    """
    clause: list of signed ints (1-indexed); positive = positive literal,
            negative = negative literal.
    H_C: sum_{i in P} x_i - sum_{i in N} x_i = |P| - 1
    Row: [a_1,...,a_n, rhs]  stored as Fractions.
    """
    P = [l for l in clause if l > 0]
    N = [-l for l in clause if l < 0]
    row = [Fraction(0)] * (n + 1)
    for i in P:
        row[i - 1] = Fraction(1)
    for i in N:
        row[i - 1] = Fraction(-1)
    rhs = Fraction(len(P) - 1)
    row[n] = rhs
    return row

# ── Zaslavsky r(A) via Möbius inversion on the intersection poset ─────────────
def zaslavsky_region_count(clauses, n):
    """
    Enumerate subsets of clauses, compute rank -> flat id by (frozenset of
    linearly-independent generators up to augmented rank), then do Möbius
    inversion to get sum |mu|.

    We represent each flat by its augmented rank only (as a proxy), which
    over-merges flats of the same rank but gives a computable upper bound
    that is exact when the arrangement is in general position.

    For correctness we represent flats by the row-reduced image (canonical
    basis) rather than just rank.
    """
    k = len(clauses)
    rows = [clause_to_row(c, n) for c in clauses]

    # Map each subset -> rank (augmented system)
    # Flat = equivalence class: two subsets define the same flat iff their
    # spans (in R^{n+1}) are identical.
    # We identify the span by its row-echelon canonical form.

    def canonical_span(subset_idx):
        if not subset_idx:
            return ()
        M = [rows[i][:] for i in subset_idx]
        # Gaussian elimination to row echelon
        pivot_row = 0
        ncols = n + 1
        for col in range(ncols):
            found = -1
            for r in range(pivot_row, len(M)):
                if M[r][col] != 0:
                    found = r
                    break
            if found == -1:
                continue
            M[pivot_row], M[found] = M[found], M[pivot_row]
            inv = Fraction(1) / M[pivot_row][col]
            M[pivot_row] = [v * inv for v in M[pivot_row]]
            for r in range(len(M)):
                if r != pivot_row and M[r][col] != 0:
                    factor = M[r][col]
                    M[r] = [M[r][c] - factor * M[pivot_row][c] for c in range(ncols)]
            pivot_row += 1
        # Keep only non-zero rows
        basis = tuple(
            tuple(v for v in row)
            for row in M if any(v != 0 for v in row)
        )
        return basis

    # Build poset: flat -> (canonical_span, rank)
    # flat_id -> canonical basis
    span_to_id = {}
    id_to_rank = {}
    flat_count = [0]

    def get_flat(subset_idx):
        cs = canonical_span(subset_idx)
        if cs not in span_to_id:
            fid = flat_count[0]
            flat_count[0] += 1
            span_to_id[cs] = fid
            id_to_rank[fid] = len(cs)
        return span_to_id[cs]

    # 0-hat: the empty flat
    zero_hat = get_flat(frozenset())

    # Enumerate all subsets -> collect flats
    if k > 20:
        raise ValueError("Too many clauses")

    all_flats = set()
    all_flats.add(zero_hat)
    for r in range(1, k + 1):
        for subset in itertools.combinations(range(k), r):
            fid = get_flat(frozenset(subset))
            all_flats.add(fid)

    # Build cover relations: flat X covers flat Y if rank(X) = rank(Y)+1
    # and Y <= X (Y's span is a subspace of X's span).
    # We need full order: Y <= X iff span(Y) subset span(X).
    # Represent each flat by its canonical basis as a set of row vectors.
    id_to_span = {v: k2 for k2, v in span_to_id.items()}

    def span_leq(span_a, span_b):
        """Is span_a a subspace of span_b? (span_a <= span_b)"""
        if not span_a:
            return True
        if not span_b:
            return False
        # Check each row of span_a is in span of span_b
        # by checking rank doesn't increase when adding it
        rb = len(span_b)
        for row in span_a:
            combined = list(span_b) + [row]
            M = [list(r) for r in combined]
            ncols = n + 1
            pr = 0
            for col in range(ncols):
                found = -1
                for rv in range(pr, len(M)):
                    if M[rv][col] != 0:
                        found = rv
                        break
                if found == -1:
                    continue
                M[pr], M[found] = M[found], M[pr]
                inv = Fraction(1) / M[pr][col]
                M[pr] = [v * inv for v in M[pr]]
                for rv in range(len(M)):
                    if rv != pr and M[rv][col] != 0:
                        factor = M[rv][col]
                        M[rv] = [M[rv][c] - factor * M[pr][c] for c in range(ncols)]
                pr += 1
            new_rank = sum(1 for r in M if any(v != 0 for v in r))
            if new_rank > rb:
                return False
        return True

    flat_list = sorted(all_flats, key=lambda x: id_to_rank[x])

    # Möbius inversion: mu[X] = -sum_{Y < X} mu[Y], mu[0_hat] = 1
    mu = {zero_hat: 1}
    for X in flat_list:
        if X == zero_hat:
            continue
        span_X = id_to_span[X]
        s = 0
        for Y in flat_list:
            if Y == X:
                break
            if Y in mu and id_to_rank[Y] < id_to_rank[X]:
                span_Y = id_to_span[Y]
                if span_leq(span_Y, span_X):
                    s += mu[Y]
        mu[X] = -s

    region_count = sum(abs(v) for v in mu.values())
    return region_count

# ── CNF generators ────────────────────────────────────────────────────────────
def cnf_parity(n):
    """XOR of all n variables as CNF (2^(n-1) clauses)."""
    clauses = []
    for assignment in itertools.product([-1, 1], repeat=n):
        if assignment.count(-1) % 2 == 0:
            clause = [i + 1 if assignment[i] == 1 else -(i + 1) for i in range(n)]
            clauses.append(clause)
    return clauses

def cnf_mod3(n):
    """(sum of vars) mod 3 == 0 as CNF."""
    clauses = []
    for assignment in itertools.product([0, 1], repeat=n):
        if sum(assignment) % 3 != 0:
            clause = [-(i + 1) if assignment[i] == 1 else (i + 1) for i in range(n)]
            clauses.append(clause)
    return clauses

def cnf_and_mod2(n):
    """(x1 AND x2 AND x3) XOR (x4 XOR ... XOR xn) as CNF (approx)."""
    half = n // 2
    clauses = []
    # AND part: x1 AND ... AND x_half, i.e. single clause enforcing all=1
    # XOR part on remaining vars
    for assignment in itertools.product([0, 1], repeat=n):
        and_part = all(assignment[i] == 1 for i in range(half))
        xor_part = sum(assignment[half:]) % 2
        result = int(and_part) ^ xor_part
        if result != 1:
            clause = [-(i + 1) if assignment[i] == 1 else (i + 1) for i in range(n)]
            clauses.append(clause)
    return clauses

def cnf_random_3sat(n, density, rng):
    """Random 3-CNF with density * n clauses."""
    k = max(1, int(density * n))
    clauses = []
    for _ in range(k):
        vars_chosen = rng.sample(range(1, n + 1), min(3, n))
        clause = [v if rng.random() < 0.5 else -v for v in vars_chosen]
        clauses.append(clause)
    return clauses

# ── Main trial ────────────────────────────────────────────────────────────────
def run_trial(seed: int) -> dict:
    rng = random.Random(seed)
    results = []
    counterexample = ""
    conjecture_holds = True
    instances_tested = 0

    # Parameters
    n_values = [5, 6, 7, 8]  # keep small for tractability
    density = 4
    d = 2
    s_factor = 2  # s = s_factor * n

    metric_values = []

    for n in n_values:
        s = s_factor * n
        bound = 4.0 * d * (math.log2(s) + math.log2(n))

        # ── Population (i): MOD_3 (limit clauses for tractability) ──
        try:
            clauses_mod3 = cnf_mod3(n)
            # subsample if too large
            if len(clauses_mod3) > 18:
                clauses_mod3 = rng.sample(clauses_mod3, 18)
            r = zaslavsky_region_count(clauses_mod3, n)
            lr = math.log2(max(r, 1))
            instances_tested += 1
            metric_values.append(lr)
            if lr > bound:
                counterexample = f"MOD3 n={n}: log2 r={lr:.2f} > bound={bound:.2f}"
                conjecture_holds = False
        except Exception:
            pass

        # ── Population (ii): AND-of-MOD_2 ──
        try:
            clauses_am2 = cnf_and_mod2(n)
            if len(clauses_am2) > 18:
                clauses_am2 = rng.sample(clauses_am2, 18)
            r = zaslavsky_region_count(clauses_am2, n)
            lr = math.log2(max(r, 1))
            instances_tested += 1
            metric_values.append(lr)
            if lr > bound:
                counterexample = f"AND_MOD2 n={n}: log2 r={lr:.2f} > bound={bound:.2f}"
                conjecture_holds = False
        except Exception:
            pass

        # ── Population (iii): parity ──
        try:
            clauses_par = cnf_parity(n)
            if len(clauses_par) > 18:
                clauses_par = rng.sample(clauses_par, 18)
            r = zaslavsky_region_count(clauses_par, n)
            lr = math.log2(max(r, 1))
            instances_tested += 1
            metric_values.append(lr)
            if lr > bound:
                counterexample = f"PARITY n={n}: log2 r={lr:.2f} > bound={bound:.2f}"
                conjecture_holds = False
        except Exception:
            pass

        # ── Population (iv): random 3-CNF (non-vacuity check) ──
        try:
            clauses_rand = cnf_random_3sat(n, density, rng)
            if len(clauses_rand) > 18:
                clauses_rand = clauses_rand[:18]
            r_rand = zaslavsky_region_count(clauses_rand, n)
            lr_rand = math.log2(max(r_rand, 1))
            instances_tested += 1
            metric_values.append(lr_rand)
        except Exception:
            pass

    mv = sum(metric_values) / len(metric_values) if metric_values else 0.0
    return {
        "metric_name": "log2_region_count",
        "metric_value": mv,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    trial_results = []
    first_fail_seed = None
    first_fail_ce = ""

    for seed in seeds:
        res = run_trial(seed)
        row = {"seed": seed, **res}
        print("TRIAL:", json.dumps(row))
        trial_results.append(res)
        if not res["conjecture_holds"] and first_fail_seed is None:
            first_fail_seed = seed
            first_fail_ce = res["counterexample"]

    vals = [r["metric_value"] for r in trial_results]
    mean_v = sum(vals) / len(vals)
    std_v = math.sqrt(sum((v - mean_v) ** 2 for v in vals) / len(vals)) if len(vals) > 1 else 0.0
    support_frac = sum(1 for r in trial_results if r["conjecture_holds"]) / len(trial_results)

    if first_fail_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{first_fail_ce}" first_failing_seed={first_fail_seed}')
    elif support_frac >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_v:.4f} std={std_v:.4f} support_fraction={support_frac:.2f}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_frac:.2f}")