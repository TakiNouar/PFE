COMMENT
InhEv: event-driven GABA-A synapse for BLA Run 1, main level (DEV-007).

One InhEv per receiving compartment collects every inhibitory connection of one
pathway type. It reproduces, connection by connection, Feng et al. 2019's
interD2pyrD_STFD / interD2interD_STFD (ModelDB 247968): the Destexhe 1994 kinetic
scheme with a pulse ending Cdur after the last spike, one weight W per connection,
and short-term depression that rescales the connection's whole conductance at each
spike (fac = max(floor, D1*D2), then D1 *= d1, D2 *= d2). Feng's inert long-term
plasticity term is not included. Method: Destexhe, Mainen & Sejnowski 1994
(Neural Comput 6:14-18), as in ExcEv.

Defaults are Feng's FSI->PN values; FSI->FSI values are set from Python.
ENDCOMMENT

NEURON {
    POINT_PROCESS InhEv
    NONSPECIFIC_CURRENT i
    RANGE Cdur, AlphaTmax, Beta, Erev, gbar
    RANGE d1, tauD1, d2, tauD2, fac_floor
    RANGE g
    THREADSAFE
}

UNITS {
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (uS) = (microsiemens)
}

PARAMETER {
    Cdur = 0.7254 (ms)
    AlphaTmax = 1.52 (/ms)
    Beta = 0.14 (/ms)
    Erev = -75 (mV)
    gbar = 0.6e-3 (uS)
    d1 = 0.95
    tauD1 = 40 (ms)
    d2 = 0.9
    tauD2 = 70 (ms)
    fac_floor = 0.7
}

ASSIGNED {
    dt (ms)
    v (mV)
    i (nA)
    g (uS)
    synon
    Rinf
    Rtau (ms)
}

STATE { Gon Goff }

INITIAL {
    Rinf = AlphaTmax / (AlphaTmax + Beta)
    Rtau = 1 / (AlphaTmax + Beta)
    synon = 0
    Gon = 0
    Goff = 0
}

BREAKPOINT {
    SOLVE release METHOD cnexp
    g = gbar * (Gon + Goff)
    i = g * (v - Erev)
}

DERIVATIVE release {
    Gon' = (synon * Rinf - Gon) / Rtau
    Goff' = -Beta * Goff
}

FUNCTION tgrid(te (ms)) (ms) {
    : Fixed-step NEURON applies an event arriving at te from the step that starts at the
    : grid point nearest te (events up to t + dt/2 are delivered at t). The summed states
    : switch there, so each connection's own fraction is evaluated at that grid time.
    tgrid = -dt * floor(-(te / dt - 0.5 - 1e-9))
}

UNITSOFF
NET_RECEIVE(W, fac, D1, D2, tsyn, nspk, on, r0, t0) {
    LOCAL r, fnew, tg
    INITIAL {
        fac = 1
        D1 = 1
        D2 = 1
        tsyn = 0
        nspk = 0
        on = 0
        r0 = 0
        t0 = 0
    }
    tg = tgrid(t)
    if (flag == 0) {
        D1 = 1 - (1 - D1) * exp(-(t - tsyn) / tauD1)
        D2 = 1 - (1 - D2) * exp(-(t - tsyn) / tauD2)
        tsyn = t
        fnew = D1 * D2
        if (fnew < fac_floor) {
            fnew = fac_floor
        }
        D1 = D1 * d1
        D2 = D2 * d2
        if (on == 1) {
            r = Rinf + (r0 - Rinf) * exp(-(tg - t0) / Rtau)
            Gon = Gon + W * (fnew - fac) * r
            synon = synon + W * (fnew - fac)
        } else {
            r = r0 * exp(-Beta * (tg - t0))
            Goff = Goff - W * fac * r
            Gon = Gon + W * fnew * r
            synon = synon + W * fnew
            on = 1
        }
        r0 = r
        t0 = tg
        fac = fnew
        nspk = nspk + 1
        net_send(Cdur, nspk)
    } else {
        if (flag == nspk && on == 1) {
            r = Rinf + (r0 - Rinf) * exp(-(tg - t0) / Rtau)
            Gon = Gon - W * fac * r
            Goff = Goff + W * fac * r
            synon = synon - W * fac
            on = 0
            r0 = r
            t0 = tg
        }
    }
}
UNITSON
