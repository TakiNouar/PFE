# Simulation Tests

Isolated and multi-region simulation studies for the biophysical limbic network.

## Folder Structure

| Folder | Purpose |
|--------|---------|
| **BLA/** | Basolateral Amygdala — isolated characterization (Runs 1–5 complete; Run 6 pending with Feng et al. 2019 parameters) |
| **CeA/** | Central Amygdala — isolation study (next) |
| **PFC/** | Prefrontal Cortex |
| **HYP/** | Hypothalamus |
| **HIP/** | Hippocampus |
| **INS/** | Insula |
| **ACC/** | Anterior Cingulate |
| **NAc/** | Nucleus Accumbens |
| **VTA/** | Ventral Tegmental Area |
| **PAG/** | Periaqueductal Gray / brainstem |
| **Neurons Connected/** | Multi-region / full-network simulations (BLA→CeA two-region, then full 10-region wiring) |

## Strategy

**Isolation-first:** characterize each region independently with literature-grounded parameters, then wire networks under `Neurons Connected/`.

Reports and findings live in `Research/reports/`.
Sources and parameters live in `Research/Sources/`.
