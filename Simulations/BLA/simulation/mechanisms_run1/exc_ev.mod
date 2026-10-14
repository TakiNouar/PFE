COMMENT
ExcEv: event-driven AMPA + NMDA synapse for BLA Run 1, main level (DEV-007).

One ExcEv per receiving compartment collects every excitatory connection of one
pathway type. It reproduces, connection by connection, Feng et al. 2019's
pyrD2pyrD_STFD / pyrD2interD_STFD (ModelDB 247968):
  - Destexhe, Mainen & Sejnowski 1994 kinetic scheme r' = AlphaTmax*on*(1-r) - Beta*r,
    with a transmitter pulse that ends Cdur after the LAST spike of that connection;
  - one weight W per connection, shared by AMPA and NMDA;
  - NMDA Mg block s(V) = 1/(1 + 0.33 exp(-0.06 V)) (Zador et al. 1990);
  - short-term depression: at each spike D1, D2 recover (tauD1, tauD2), the release
    factor fac = max(floor, D1*D2) is set, then D1 *= d1, D2 *= d2; fac rescales the
    connection's WHOLE conductance from that spike on, as in Feng's code.
Feng's inert long-term plasticity term (x1e-12) is not included.

Method: the exact event-driven algorithm of Destexhe, Mainen & Sejnowski 1994
(Neural Comput 6:14-18). Ron/Roff hold the summed weighted open fractions of the
connections whose pulse is on / off; each connection's own fraction is computed
analytically only when one of its events arrives. Per-connection state lives in the
NetCon weight vector (see NET_RECEIVE arguments).

Defaults are Feng's PN->PN values; PN->FSI values are set from Python.
ENDCOMMENT

NEURON {
    POINT_PROCESS ExcEv
    NONSPECIFIC_CURRENT i
    RANGE Cdur_a, AlphaTmax_a, Beta_a, Erev_a, gbar_a
    RANGE Cdur_n, AlphaTmax_n, Beta_n, Erev_n, gbar_n
    RANGE d1, tauD1, d2, tauD2, fac_floor
    RANGE g_a, g_n, i_a, i_n
    THREADSAFE
}

UNITS {
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (uS) = (microsiemens)
}

PARAMETER {
    Cdur_a = 1.4210 (ms)
    AlphaTmax_a = 3.8142 (/ms)
    Beta_a = 0.1429 (/ms)
    Erev_a = 0 (mV)
    gbar_a = 1e-3 (uS)
    Cdur_n = 16.7650 (ms)
    AlphaTmax_n = 0.2659 (/ms)
    Beta_n = 0.008 (/ms)
    Erev_n = 0 (mV)
    gbar_n = 0.5e-3 (uS)
    d1 = 0.95
    tauD1 = 40 (ms)
    d2 = 0.9
    tauD2 = 70 (ms)
    fac_floor = 0.5
}

ASSIGNED {
    dt (ms)
    v (mV)
    i (nA)
    i_a (nA)
    i_n (nA)
    g_a (uS)
    g_n (uS)
    synon_a
    synon_n
    Rinf_a
    Rtau_a (ms)
    Rinf_n
    Rtau_n (ms)
}

STATE { Aon Aoff Non Noff }

INITIAL {
    Rinf_a = AlphaTmax_a / (AlphaTmax_a + Beta_a)
    Rtau_a = 1 / (AlphaTmax_a + Beta_a)
    Rinf_n = AlphaTmax_n / (AlphaTmax_n + Beta_n)
    Rtau_n = 1 / (AlphaTmax_n + Beta_n)
    synon_a = 0
    synon_n = 0
    Aon = 0
    Aoff = 0
    Non = 0
    Noff = 0
}

BREAKPOINT {
    SOLVE release METHOD cnexp
    g_a = gbar_a * (Aon + Aoff)
    g_n = gbar_n * (Non + Noff)
    i_a = g_a * (v - Erev_a)
    i_n = g_n * (v - Erev_n) * sfunc(v)
    i = i_a + i_n
}

DERIVATIVE release {
    Aon' = (synon_a * Rinf_a - Aon) / Rtau_a
    Aoff' = -Beta_a * Aoff
    Non' = (synon_n * Rinf_n - Non) / Rtau_n
    Noff' = -Beta_n * Noff
}

FUNCTION sfunc(v (mV)) {
    UNITSOFF
    sfunc = 1 / (1 + 0.33 * exp(-0.06 * v))
    UNITSON
}

FUNCTION tgrid(te (ms)) (ms) {
    : Fixed-step NEURON applies an event arriving at te from the step that starts at the
    : grid point nearest te (events up to t + dt/2 are delivered at t). The summed states
    : switch there, so each connection's own fraction is evaluated at that grid time.
    tgrid = -dt * floor(-(te / dt - 0.5 - 1e-9))
}

UNITSOFF
: Per-connection state: W weight; fac current release factor; D1, D2, tsyn depression;
: nspk spike count (identifies the latest pulse); ona/onn pulse on; ra0/rn0 open
: fraction at time ta0/tn0. Off events: flag = +nspk (AMPA), -nspk (NMDA); only the
: latest spike's off event acts, so a pulse ends Cdur after the last spike.
NET_RECEIVE(W, fac, D1, D2, tsyn, nspk, ona, ra0, ta0, onn, rn0, tn0) {
    LOCAL ra, rn, fnew, tg
    INITIAL {
        fac = 1
        D1 = 1
        D2 = 1
        tsyn = 0
        nspk = 0
        ona = 0
        ra0 = 0
        ta0 = 0
        onn = 0
        rn0 = 0
        tn0 = 0
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

        if (ona == 1) {
            ra = Rinf_a + (ra0 - Rinf_a) * exp(-(tg - ta0) / Rtau_a)
            Aon = Aon + W * (fnew - fac) * ra
            synon_a = synon_a + W * (fnew - fac)
        } else {
            ra = ra0 * exp(-Beta_a * (tg - ta0))
            Aoff = Aoff - W * fac * ra
            Aon = Aon + W * fnew * ra
            synon_a = synon_a + W * fnew
            ona = 1
        }
        ra0 = ra
        ta0 = tg

        if (onn == 1) {
            rn = Rinf_n + (rn0 - Rinf_n) * exp(-(tg - tn0) / Rtau_n)
            Non = Non + W * (fnew - fac) * rn
            synon_n = synon_n + W * (fnew - fac)
        } else {
            rn = rn0 * exp(-Beta_n * (tg - tn0))
            Noff = Noff - W * fac * rn
            Non = Non + W * fnew * rn
            synon_n = synon_n + W * fnew
            onn = 1
        }
        rn0 = rn
        tn0 = tg

        fac = fnew
        nspk = nspk + 1
        net_send(Cdur_a, nspk)
        net_send(Cdur_n, -nspk)
    } else if (flag > 0) {
        if (flag == nspk && ona == 1) {
            ra = Rinf_a + (ra0 - Rinf_a) * exp(-(tg - ta0) / Rtau_a)
            Aon = Aon - W * fac * ra
            Aoff = Aoff + W * fac * ra
            synon_a = synon_a - W * fac
            ona = 0
            ra0 = ra
            ta0 = tg
        }
    } else {
        if (-flag == nspk && onn == 1) {
            rn = Rinf_n + (rn0 - Rinf_n) * exp(-(tg - tn0) / Rtau_n)
            Non = Non - W * fac * rn
            Noff = Noff + W * fac * rn
            synon_n = synon_n - W * fac
            onn = 0
            rn0 = rn
            tn0 = tg
        }
    }
}
UNITSON
