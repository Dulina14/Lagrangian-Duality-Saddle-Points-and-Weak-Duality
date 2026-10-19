"""
EN3330 Assignment 03 - plots for Q1, Q2, Q3
Problem: min x^2  s.t. x >= 1   ->  h(x) = 1 - x <= 0
Lagrangian: L(mu, x) = x^2 + mu*(1 - x),  mu >= 0
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# Save all figures into <repo>/figures, whatever folder the script is run from
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)
os.chdir(FIG_DIR)

plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3})

def L(mu, x):
    return x**2 + mu * (1 - x)

def d(mu):                      # dual function, derived in Q1(b)
    return mu - mu**2 / 4

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

# ---------------- Q1(a): L(mu, x) vs x for mu = 0,1,2,3 ----------------
x = np.linspace(-1, 3, 400)
fig, ax = plt.subplots(figsize=(7, 4.5))
for mu, c in zip([0, 1, 2, 3], colors):
    ax.plot(x, L(mu, x), color=c, label=fr"$\mu={mu}$")
    xm = mu / 2                                  # minimizer x(mu) = mu/2
    ax.plot(xm, L(mu, xm), "o", color=c, ms=8)
    off = {0: (6, -16), 1: (-30, -22), 2: (8, 8), 3: (6, -18)}[mu]
    ax.annotate(fr"$x({mu})={xm:g}$", (xm, L(mu, xm)),
                textcoords="offset points", xytext=off, color=c)
ax.axvline(1, color="k", ls="--", lw=1, label="constraint boundary $x=1$")
ax.axvspan(-1, 1, color="grey", alpha=0.12, label="infeasible ($x<1$)")
ax.set_xlabel("$x$"); ax.set_ylabel(r"$L(\mu,x)$")
ax.set_title(r"Q1(a): $L(\mu,x)=x^2+\mu(1-x)$ and its minimizers $x(\mu)=\mu/2$")
ax.set_ylim(-0.5, 9); ax.legend(loc="upper left", fontsize=9)
fig.tight_layout(); fig.savefig("Q1a_lagrangian_vs_x.png", dpi=200)

# ---------------- Q1(b): dual function d(mu) ----------------
mu = np.linspace(0, 5, 400)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(mu, d(mu), lw=2, label=r"$d(\mu)=\mu-\mu^2/4$")
ax.plot(2, 1, "ro", ms=9, label=r"$\mu^*=2,\ d^*=1$")
ax.axhline(1, color="k", ls="--", lw=1, label=r"primal optimum $p^*=1$")
for m in [0, 1, 3]:
    ax.plot(m, d(m), "ko", ms=5)
    ax.annotate(f"d({m})={d(m):g}", (m, d(m)), textcoords="offset points",
                xytext=(6, -14))
ax.set_xlabel(r"$\mu$"); ax.set_ylabel(r"$d(\mu)$")
ax.set_title("Q1(b): Dual function (concave, maximum at $\\mu^*=2$)")
ax.set_ylim(-1.5, 1.6); ax.legend(loc="lower center", fontsize=9)
fig.tight_layout(); fig.savefig("Q1b_dual_function.png", dpi=200)

# ---------------- Q1(c): primal function g(x) = max_mu L ----------------
x = np.linspace(-1, 3, 800)
fig, ax = plt.subplots(figsize=(7, 4.5))
for m, c in zip([0, 2, 5, 20, 100], ["tab:blue", "tab:orange", "tab:green",
                                     "tab:purple", "tab:red"]):
    ax.plot(x, L(m, x), color=c, lw=1, alpha=0.8, label=fr"$L(\mu={m},x)$")
xf = x[x >= 1]
ax.plot(xf, xf**2, "k", lw=3, label=r"$g(x)=x^2$ (feasible, best $\mu=0$)")
ax.axvspan(-1, 1, color="grey", alpha=0.15)
ax.text(-0.85, 13, r"$g(x)=+\infty$" "\n" r"(infeasible: $L\to\infty$ as $\mu\to\infty$)",
        fontsize=10)
ax.annotate("", xy=(-0.6, 12.5), xytext=(-0.6, 7), arrowprops=dict(arrowstyle="->", lw=2))
ax.plot(1, 1, "ro", ms=9, label=r"$\min g = 1$ at $x^*=1$")
ax.axvline(1, color="k", ls="--", lw=1)
ax.set_xlim(-1, 3); ax.set_ylim(-1, 15)
ax.set_xlabel("$x$"); ax.set_ylabel(r"$L(\mu,x)$,  $g(x)$")
ax.set_title(r"Q1(c): Primal function $g(x)=\max_{\mu\geq 0} L(\mu,x)$")
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout(); fig.savefig("Q1c_primal_function.png", dpi=200)

# ---------------- Q2(a)(iv): saddle point, two small graphs ----------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
mu = np.linspace(0, 5, 200)
a1.plot(mu, L(mu, 1.0), lw=2)
a1.plot(2, 1, "ro", ms=8, label=r"$L(\mu^*,x^*)=1$")
a1.set_xlabel(r"$\mu$"); a1.set_ylabel(r"$L(\mu,x^*)$")
a1.set_title(r"$L(\mu, x^*=1)=1$ (flat in $\mu$)"); a1.set_ylim(0, 2); a1.legend()
x = np.linspace(-1, 3, 200)
a2.plot(x, L(2, x), lw=2)
a2.plot(1, 1, "ro", ms=8, label=r"$L(\mu^*,x^*)=1$")
a2.set_xlabel("$x$"); a2.set_ylabel(r"$L(\mu^*,x)$")
a2.set_title(r"$L(\mu^*=2,x)=(x-1)^2+1$"); a2.legend()
fig.suptitle("Q2(a)(iv): $(x^*,\\mu^*)=(1,2)$ is a saddle point of $L$")
fig.tight_layout(); fig.savefig("Q2a_saddle_point.png", dpi=200)

# ---------------- Q3(b): lines in mu and their lower envelope ----------------
mu = np.linspace(0, 5, 400)
fig, ax = plt.subplots(figsize=(7, 4.5))
lines = {0: mu, 1: np.ones_like(mu), 2: 4 - mu}
names = {0: r"$x=0$: $L=\mu$", 1: r"$x=1$: $L=1$", 2: r"$x=2$: $L=4-\mu$"}
for (xv, yv), c in zip(lines.items(), ["tab:blue", "tab:orange", "tab:green"]):
    ax.plot(mu, yv, color=c, lw=1.2, label=names[xv])
env = np.minimum.reduce(list(lines.values()))
ax.plot(mu, env, "k", lw=3, label="lower envelope of the 3 lines")
ax.plot(mu, d(mu), "r--", lw=2, label=r"true $d(\mu)=\mu-\mu^2/4$")
ax.set_xlabel(r"$\mu$"); ax.set_ylabel(r"$L(\mu,x)$")
ax.set_title(r"Q3(b): $L(\mu,x)$ is a straight line in $\mu$ for each fixed $x$")
ax.set_ylim(-1.5, 4.5); ax.legend(fontsize=9, loc="upper right")
fig.tight_layout(); fig.savefig("Q3b_lower_envelope.png", dpi=200)

print("All figures saved.")
