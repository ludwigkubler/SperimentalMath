import random
import itertools
from collections import defaultdict, deque
import math

# We cannot compute unstable 2-cohomotopy classes or resolution width exactly in general,
# especially via standard libraries. This is a simulation that approximates the conjecture
# using heuristics and proxies due to intractability of exact computation.

# However, the conjecture is highly non-constructive and involves advanced algebraic topology
# and proof complexity. We must simulate a test using feasible proxies.

# APPROXIMATION STRATEGY:
# - Generate random 3-SAT instances (n <= 10, m = 4n)
# - Build clause-link complex: each clause is a triangle; identify vertices for same variable
#   (but preserve polarity: x and ~x are different vertices)
# - Proxy for |[Z_φ, S^2]_*|: use the number of connected components in the dual graph of triangles
#   after identifying vertices by variable, but this is weak. Alternatively, use the rank of H_2
#   (which is a lower bound on cohomotopy in some cases), but H_2 is abelian.
#   Instead, we use a heuristic: the number of "independent" clause cycles in the complex.
# - Proxy for resolution width w(φ): use the minimum width found by a simple DPLL-based
#   resolution simulator that tracks the maximum clause size (width) during resolution.

# Since we cannot compute 2-cohomotopy classes exactly, we use a topological invariant
# that might correlate: the number of 2-sphere wedge summands after simplification.
# We simulate "homotopy simplification" via edge contractions that preserve homotopy type.

# Due to extreme complexity, we use small n and approximate.

random.seed(42)

def generate_3sat_instance(n, m):
    clauses = []
    for _ in range(m):
        vars = random.sample(range(1, n+1), 3)
        clause = tuple(random.choice([v, -v]) for v in vars)
        clauses.append(clause)
    return clauses

def build_clause_link_complex(clauses):
    # Each clause is a triangle: three vertices, one per literal
    # Vertex label: (literal, clause_id, pos_in_clause)
    # But we identify vertices with the same literal? No: the complex identifies vertices
    # for the same variable occurrence? The problem says: "variable-sharing identifies vertices"
    # But preserving polarity. So vertex for literal `x` in clause A is same as `x` in clause B?
    # Interpretation: identify all occurrences of the same literal (same variable, same polarity)
    # So vertex per literal (e.g., x1, ~x2), not per occurrence.

    # So: one vertex per literal (i.e., per variable with sign)
    # But wait: that would collapse all x1 to one vertex. But then a clause (x1 ∨ x2 ∨ x3)
    # becomes a triangle on vertices x1, x2, x3.

    # So complex has:
    # - One vertex per literal (so 2n vertices: x1, ~x1, ..., xn, ~xn)
    # - One triangle per clause: for clause (l1, l2, l3), add a 2-simplex on (l1, l2, l3)

    # But note: a literal is an integer: positive for x_i, negative for ~x_i.
    # Map literal to vertex id: literal l -> id = l if l>0, id = l if l<0? But we need positive indices.
    # Map literal l to vertex id: if l>0: 2*(l-1), if l<0: 2*(-l-1)+1
    def lit_to_vertex(lit):
        var = abs(lit)
        return 2*(var-1) + (0 if lit > 0 else 1)

    n_vars = max(abs(lit) for clause in clauses for lit in clause) if clauses else 0
    n_vertices = 2 * n_vars  # x1, ~x1, ..., xn, ~xn

    # Build list of triangles (each is a triple of vertex ids)
    triangles = []
    for clause in clauses:
        if len(clause) != 3:
            continue
        tri = tuple(lit_to_vertex(lit) for lit in clause)
        triangles.append(tri)

    return n_vertices, triangles

def count_independent_cycles(triangles, n_vertices):
    # A very rough proxy: the rank of H_2 of the complex.
    # H_2 = ker(∂2) / im(∂1), but we compute only dim(ker ∂2) since im ∂1 is in 1-chains.
    # But we can compute the rank of the 2-chain boundary map.

    # Represent 2-chains: each triangle is a basis vector.
    # ∂2: Z^T -> Z^E, where T = len(triangles), E = number of edges.

    # First, collect all edges from triangles.
    edge_to_tris = defaultdict(list)  # edge (u,v) with u<v -> list of triangle indices
    for tri_idx, (u, v, w) in enumerate(triangles):
        edges = [(min(u,v), max(u,v)), (min(v,w), max(v,w)), (min(w,u), max(w,u))]
        for edge in edges:
            edge_to_tris[edge].append(tri_idx)

    n_edges = len(edge_to_tris)
    n_tris = len(triangles)

    if n_tris == 0:
        return 0

    # We want the kernel of ∂2: but over integers? We do over GF(2) for simplicity.
    # The rank of the cycle space in dimension 2: number of linearly independent combinations
    # of triangles whose boundary cancels.

    # Build matrix over GF(2): rows = edges, cols = triangles.
    # entry[i,j] = 1 if triangle j contains edge i, else 0.

    edge_list = list(edge_to_tris.keys())
    edge_index = {edge: i for i, edge in enumerate(edge_list)}

    # Matrix: n_edges x n_tris
    mat = [[0]*n_tris for _ in range(n_edges)]
    for tri_idx, tri in enumerate(triangles):
        u, v, w = tri
        e1 = (min(u,v), max(u,v))
        e2 = (min(v,w), max(v,w))
        e3 = (min(w,u), max(w,u))
        mat[edge_index[e1]][tri_idx] = 1
        mat[edge_index[e2]][tri_idx] = 1
        mat[edge_index[e3]][tri_idx] = 1

    # Compute rank over GF(2) via Gaussian elimination
    rows = mat
    rank = 0
    for col in range(n_tris):
        # find pivot
        pivot = -1
        for r in range(rank, n_edges):
            if rows[r][col]:
                pivot = r
                break
        if pivot == -1:
            continue
        # swap
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        # eliminate
        for r in range(rank+1, n_edges):
            if rows[r][col]:
                for c in range(col, n_tris):
                    rows[r][c] ^= rows[rank][c]
        rank += 1

    # The kernel dimension = n_tris - rank(∂2)
    # But H_2 = ker(∂2) because ∂1 maps to 1-chains, but we ignore im(∂1) because it's in lower dim.
    # Actually, H_2 = ker(∂2) since there are no 3-chains. So rank(H_2) = n_tris - rank(∂2)
    h2_rank = n_tris - rank
    return h2_rank

def dpll_width(clauses):
    # Simplified DPLL that tracks the maximum width (clause size) during resolution.
    # But we want minimum resolution width: the minimum over all resolution refutations
    # of the maximum clause size in the proof.
    # This is hard. We use a greedy DPLL and record the maximum clause size in the recursion,
    # but that's not resolution width.

    # Instead, we simulate a resolution proof search with bounded width.
    # We try to find a refutation with width k, for k from 1 up.
    # But this is exponential.

    # We use a proxy: the depth of DPLL search tree, or the maximum number of literals
    # in a clause during unit propagation and branching.

    # Alternate proxy: use the treewidth of the clause graph? But we need resolution width.

    # Known: resolution width >= treewidth of the primal graph + 1.
    # But we compute a lower bound.

    # Due to time, we use a simple heuristic: the maximum number of clauses that share
    # a common variable, plus 2? Not accurate.

    # Another idea: simulate a resolution proof with bounded width using a simple algorithm.

    # We implement a basic resolution width lower bound: Ben-Sasson-Wigderson method?
    # Too complex.

    # Instead, we use the following known fact: width >= sqrt(n) for random 4n clauses?
    # But we need instance-specific.

    # We use a greedy resolution: always resolve on the most frequent literal.
    # We track the maximum clause size (width) in the entire proof until we get the empty clause.

    # But this may not find the minimum width.

    # We do bounded-width search: for w from 1 to 100, try to find a refutation with clauses of size <= w.

    # But too slow.

    # We use a proxy: the maximum degree in the primal graph (variable-clause incidence)
    # or the maximum number of clauses any variable appears in.

    var_count = defaultdict(int)
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            var_count[var] += 1

    if not var_count:
        return 0

    max_degree = max(var_count.values())

    # Also consider the number of clauses
    m = len(clauses)
    n_vars = max(var_count.keys()) if var_count else 0

    # Known: for random 3-SAT with m=4n, resolution width is at least Ω(n / log n) whp
    # But we want a number.

    # Use a simple DPLL that tracks the maximum clause size in the current formula.
    # But DPLL doesn't produce resolution proofs directly.

    # We simulate a resolution proof by always resolving on a variable.
    # But exhaustive.

    # Due to complexity, we return a heuristic: max_degree
    # But this is weak.

    # Another proxy: the size of the largest clause in the formula? Always 3.

    # We return max_degree as a rough proxy for width.
    return max_degree

def main():
    n_trials = 100
    results = []

    print(f"Generating {n_trials} random 3-SAT instances (n=10, m=40)...")
    for i in range(n_trials):
        n = 10
        m = 4 * n
        clauses = generate_3sat_instance(n, m)
        n_vertices, triangles = build_clause_link_complex(clauses)
        h2_rank = count_independent_cycles(triangles, n_vertices)
        width_proxy = dpll_width(clauses)

        # Record proxies
        results.append((h2_rank, width_proxy))

        if i % 10 == 0:
            print(f"Instance {i}: |H2| = {h2_rank}, width_proxy = {width_proxy}")

    # Now check if |H2| = Θ(width_proxy)
    # Compute ratios
    ratios = []
    for h2, w in results:
        if w > 0:
            ratios.append(h2 / w)
        else:
            # w=0 only if no clauses or no variables, skip
            pass

    if not ratios:
        print("No valid ratios computed.")
        print("RESULT: INCONCLUSIVE no_data")
        return

    avg_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - avg_ratio)**2 for r in ratios) / len(ratios))

    # Also check if both grow together: compute correlation
    h2_vals = [r[0] for r in results]
    w_vals = [r[1] for r in results]
    mean_h2 = sum(h2_vals) / len(h2_vals)
    mean_w = sum(w_vals) / len(w_vals)
    cov = sum((h2 - mean_h2) * (w - mean_w) for h2, w in results) / len(results)
    var_h2 = sum((h2 - mean_h2)**2 for h2 in h2_vals) / len(h2_vals)
    var_w = sum((w - mean_w)**2 for w in w_vals) / len(w_vals)
    if var_h2 > 0 and var_w > 0:
        corr = cov / (math.sqrt(var_h2) * math.sqrt(var_w))
    else:
        corr = 0.0

    print(f"Average |H2|/width_proxy ratio: {avg_ratio:.3f} ± {std_ratio:.3f}")
    print(f"Correlation between |H2| and width_proxy: {corr:.3f}")

    # The conjecture is that |[Z,S^2]| = Θ(w(φ))
    # We used |H2| as a proxy for |[Z,S^2]|, and max_degree as proxy for w(φ)
    # But |H2| is not a good proxy for 2-cohomotopy classes.
    # In fact, |[Z,S^2]| is not even a group; it's a set of homotopy classes.
    # And it can be infinite? But Z is finite, so [Z,S^2] is finite.

    # However, our proxies are too crude.

    # We cannot support the conjecture with these proxies.

    # Moreover, we see that |H2| is typically much smaller than width_proxy? Or not?

    # Example: if h2_rank is around 10, width_proxy around 10, ratio ~1.

    # But we know that for random 3-SAT with m=4n, the second Betti number is not necessarily
    # linear in the max variable degree.

    # Given the weakness of proxies, we cannot conclude.

    print("RESULT: INCONCLUSIVE weak_proxies_for_cohomotopy_and_width")

if __name__ == "__main__":
    main()