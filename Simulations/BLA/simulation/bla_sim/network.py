"""Network construction for Run 1 (architecture/02, 04, 05).

Two levels share every random draw (placement, wiring, weights, delays, gaps,
afferents, noise), so they differ only in the cells and synapses:
  "full":    Feng's cell templates and Feng's synapse files, one object per connection;
  "reduced": the main-level PN named in config "main_level_cell" (coarse_d2_p3, DEV-006),
             Feng's FSI template, event-driven synapses (DEV-007), one ExcEv / InhEv object
             per receiving cell and source class.
"""
import math

import numpy as np

from . import cells as C

STREAMS = {"placement": 1, "wiring": 2, "weights": 3, "delays": 4, "gaps": 5,
           "aff_targets": 6, "aff_weights": 7, "threat": 8, "metrics": 9,
           "probes": 10}                      # live viewer's probe cells (display only)

PATHWAYS = ("PN_PN", "FSI_PN", "PN_FSI", "FSI_FSI")
PATH_CODE = {p: i for i, p in enumerate(PATHWAYS)}
FENG_SYNAPSE = {"PN_PN": "pyrD2pyrD_STFD", "PN_FSI": "pyrD2interD_STFD",
                "FSI_PN": "interD2pyrD_STFD", "FSI_FSI": "interD2interD_STFD"}
LEVELS = ("full", "reduced")


def stream(seed, name):
    """Named, independent random stream derived from the global seed."""
    return np.random.default_rng(np.random.SeedSequence([int(seed), STREAMS[name]]))


def lognormal_params(mean, var):
    """mu, sigma of the underlying normal for NEURON's Random.lognormal(mean, variance)."""
    s2 = math.log(1.0 + var / mean ** 2)
    return math.log(mean) - s2 / 2.0, math.sqrt(s2)


def population(n_total, fractions):
    n_a = round(fractions["PN_A"] * n_total)
    n_c = round(fractions["PN_C"] * n_total)
    n_f = n_total - n_a - n_c
    types = np.array(["PN_A"] * n_a + ["PN_C"] * n_c + ["FSI"] * n_f)
    return types


def place(n_total, cfg, seed):
    """Uniform positions (mm) in a cube at Feng's density, >= 25 um apart."""
    net = cfg["network"]
    side = (n_total / net["density_per_mm3"]) ** (1.0 / 3.0)
    dmin = net["min_distance_um"] / 1000.0
    rng = stream(seed, "placement")
    pos = np.empty((n_total, 3))
    k = 0
    while k < n_total:
        cand = rng.uniform(0.0, side, size=3)
        if k == 0 or np.min(np.linalg.norm(pos[:k] - cand, axis=1)) >= dmin:
            pos[k] = cand
            k += 1
    return pos, side


def wire(types, pos, cfg, seed, dt):
    """In-degree rule (architecture/05): p = min(1, K / n_pre); weights scaled by K / n_pre if p = 1."""
    net = cfg["network"]
    pn = np.nonzero(types != "FSI")[0]
    fsi = np.nonzero(types == "FSI")[0]
    groups = {"PN": pn, "FSI": fsi}
    r_wire, r_w, r_d = stream(seed, "wiring"), stream(seed, "weights"), stream(seed, "delays")
    pre_all, post_all, path_all, w_all, d_all, scales = [], [], [], [], [], {}
    for path in PATHWAYS:
        src, dst = path.split("_")
        pre_ids, post_ids = groups[src], groups[dst]
        same = src == dst
        n_pre = len(pre_ids) - (1 if same else 0)
        K = net["in_degree"][path]
        p = min(1.0, K / n_pre)
        scale = K / n_pre if K > n_pre else 1.0
        scales[path] = {"K": K, "n_pre": n_pre, "p": p, "weight_scale": scale}
        mask = r_wire.random((len(post_ids), len(pre_ids))) < p
        if same:
            np.fill_diagonal(mask, False)          # no self-connections (Feng)
        post_idx, pre_idx = np.nonzero(mask)
        pre, post = pre_ids[pre_idx], post_ids[post_idx]
        mu, sigma = lognormal_params(*net["weight_mean_var"][path])
        w = r_w.lognormal(mu, sigma, size=len(pre)) * scale
        dist = np.linalg.norm(pos[pre] - pos[post], axis=1)
        dl = net["delay"]
        d = dist / dl["speed_mm_per_ms"] + dl["min_ms"] + r_d.uniform(-dl["jitter_ms"], dl["jitter_ms"], len(pre)) + dt
        pre_all.append(pre); post_all.append(post); path_all.append(np.full(len(pre), PATH_CODE[path]))
        w_all.append(w); d_all.append(d)
    conns = {"pre": np.concatenate(pre_all), "post": np.concatenate(post_all),
             "path": np.concatenate(path_all), "weight": np.concatenate(w_all), "delay": np.concatenate(d_all)}
    return conns, scales


def gap_pairs(types, cfg, seed):
    fsi = np.nonzero(types == "FSI")[0]
    rng = stream(seed, "gaps")
    pairs = [(a, b) for i, a in enumerate(fsi) for b in fsi[i + 1:]]
    keep = rng.random(len(pairs)) < cfg["gap_junction"]["fraction_of_FSI_pairs"]
    return [p for p, k in zip(pairs, keep) if k]


class Network:
    def __init__(self, h, cfg, n_total, level, seed):
        if level not in LEVELS:
            raise ValueError(level)
        self.h, self.cfg, self.n, self.level, self.seed = h, cfg, n_total, level, seed
        self.cell_level = "full" if level == "full" else cfg["main_level_cell"]
        self.types = population(n_total, cfg["network"]["fractions"])
        self.pos, self.side_mm = place(n_total, cfg, seed)
        self.conns, self.scales = wire(self.types, self.pos, cfg, seed, h.dt)
        self.gaps = gap_pairs(self.types, cfg, seed)
        self.pc = h.ParallelContext()
        self._keep = []
        self.cells = []
        self.syn_targets = {}     # reduced level: (gid, "rec"/"aff", "exc"/"inh") -> object
        self.netcons = {}         # pathway -> list of NetCons, for condition switches
        self.feng_syns = {}       # full level: pathway -> list of synapse objects

    # -- building -------------------------------------------------------------
    def build(self, synapses=True):
        """synapses=False builds cells and noise only (Phase 0 benchmark row): no internal
        connections and no gap junctions. The wiring is still drawn, so streams are unchanged."""
        h, pc = self.h, self.pc
        self.synapses_built = synapses
        reduced = C.load_reduced_params() if self.level == "reduced" else None
        for gid, kind in enumerate(self.types):
            cell = C.make_cell(h, kind, self.cell_level, reduced)
            self.cells.append(cell)
            pc.set_gid2node(gid, pc.id())
            nc = cell.connect2target(None)
            pc.cell(gid, nc)
            self._keep.append(nc)
        h.Random().Random123_globalindex(int(self.seed))
        for gid, kind in enumerate(self.types):
            self._keep += C.attach_noise(h, self.cells[gid], kind, gid, self.n, self.cfg)
        if synapses:
            self._connect_internal()
            self._connect_gaps()
        pc.set_maxstep(10)
        return self

    def exc_target(self, gid, cls):
        """The excitatory synapse object on a receiving cell (reduced level)."""
        key = (gid, cls, "exc")
        if key not in self.syn_targets:
            cell, kind = self.cells[gid], self.types[gid]
            obj = self.h.ExcEv(cell.dend(0.9))
            for k, v in self.cfg["event_synapses"]["PN_FSI" if kind == "FSI" else "PN_PN"].items():
                setattr(obj, k, v)
            self.syn_targets[key] = obj
        return self.syn_targets[key]

    def inh_target(self, gid):
        key = (gid, "rec", "inh")
        if key not in self.syn_targets:
            cell, kind = self.cells[gid], self.types[gid]
            obj = self.h.InhEv(cell.soma(0.5))
            for k, v in self.cfg["event_synapses"]["FSI_FSI" if kind == "FSI" else "FSI_PN"].items():
                setattr(obj, k, v)
            self.syn_targets[key] = obj
        return self.syn_targets[key]

    def _connect_internal(self):
        h, pc, c = self.h, self.pc, self.conns
        for path in PATHWAYS:
            self.netcons[path], self.feng_syns[path] = [], []
        for pre, post, code, w, d in zip(c["pre"], c["post"], c["path"], c["weight"], c["delay"]):
            path = PATHWAYS[code]
            cell = self.cells[post]
            if self.level == "full":
                sec_x = cell.soma(0.5) if path.startswith("FSI") else cell.dend(0.9)
                syn = getattr(h, FENG_SYNAPSE[path])(sec_x)
                syn.initW = float(w)
                nc = pc.gid_connect(int(pre), syn)
                nc.weight[0] = 1.0
                self.feng_syns[path].append(syn)
            else:
                tgt = self.inh_target(int(post)) if path.startswith("FSI") else self.exc_target(int(post), "rec")
                nc = pc.gid_connect(int(pre), tgt)
                nc.weight[0] = float(w)
            nc.delay = float(d)
            self.netcons[path].append(nc)

    def _connect_gaps(self):
        if not self.gaps:
            return
        h, pc = self.h, self.pc
        r = self.cfg["gap_junction"]["r_megohm"]
        base = 10 * self.n                      # source-variable ids, separate from cell gids
        for k, (a, b) in enumerate(self.gaps):
            for me, other, my_id, other_id in ((a, b, base + 2 * k, base + 2 * k + 1),
                                               (b, a, base + 2 * k + 1, base + 2 * k)):
                cell = self.cells[me]
                g = h.HalfGap(cell.soma(0.5))
                pc.target_var(g, g._ref_vgap, other_id)
                pc.source_var(cell.soma(0.5)._ref_v, my_id, sec=cell.soma)
                g.r = r
                self._keep.append(g)
        pc.setup_transfer()

    # -- condition switches (architecture/07 C5, C6) -------------------------------
    def set_pathway_weight_factor(self, path, factor):
        """Scale every connection of one pathway (0 = removed). Call before finitialize."""
        c = self.conns
        idx = np.nonzero(c["path"] == PATH_CODE[path])[0]
        if self.level == "full":
            for syn, i in zip(self.feng_syns[path], idx):
                syn.initW = float(c["weight"][i] * factor)
        else:
            for nc, i in zip(self.netcons[path], idx):
                nc.weight[0] = float(c["weight"][i] * factor)

    def set_pnpn_ampa(self, on):
        """Diagnostic C6: AMPA off on PN->PN connections only (afferents untouched)."""
        if self.level == "full":
            for syn in self.feng_syns["PN_PN"]:
                syn.gbar_ampa = 1e-3 if on else 0.0
        else:
            for (gid, cls, kind), obj in self.syn_targets.items():
                if kind == "exc" and cls == "rec" and self.types[gid] != "FSI":
                    obj.gbar_a = 1e-3 if on else 0.0

    def summary(self):
        c = self.conns
        indeg = {}
        for path in PATHWAYS:
            dst = path.split("_")[1]
            posts = np.nonzero((self.types == "FSI") if dst == "FSI" else (self.types != "FSI"))[0]
            counts = np.bincount(c["post"][c["path"] == PATH_CODE[path]], minlength=self.n)[posts]
            indeg[path] = {"mean": float(counts.mean()), "sd": float(counts.std()), **self.scales[path]}
        return {"n_total": self.n, "level": self.level, "cell_level": self.cell_level, "seed": self.seed,
                "counts": {k: int((self.types == k).sum()) for k in ("PN_A", "PN_C", "FSI")},
                "cube_side_mm": self.side_mm, "synapses_built": getattr(self, "synapses_built", True),
                "connections": int(len(c["pre"])), "in_degree": indeg,
                "gap_pairs": len(self.gaps),
                "delay_ms": {"min": float(c["delay"].min()), "mean": float(c["delay"].mean()),
                             "max": float(c["delay"].max())}}
