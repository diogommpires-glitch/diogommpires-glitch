# diogommpires-glitch

<picture>
  <source media="(max-width: 640px)" srcset="assets/profile-mobile.svg?v=purple-kitty-20261112">
  <img src="assets/profile.svg?v=purple-kitty-20261112" alt="Royal-purple public project dashboard with my kitty portrait. Eight project repositories, thirteen public snapshot commits and nine GitHub-classified source languages, checked on 12 November 2026. The project links and metric definitions follow below." width="1200">
</picture>

I build research software for sensing, machine learning and simulation. These eight public source snapshots include experiments, evaluation tools and the limits of the work.

| Project | What it explores |
| --- | --- |
| [CrossVenue](https://github.com/diogommpires-glitch/crossvenue-publication) | Market-making research, paper trading and deterministic replay |
| [Sensor Fusion](https://github.com/diogommpires-glitch/sensor-fusion-publication) | Multi-sensor positioning and state estimation |
| [Human Emotion](https://github.com/diogommpires-glitch/human-emotion-publication) | Spiking emotion-circuit simulation |
| [Wavepacket](https://github.com/diogommpires-glitch/wavepacket-publication) | Numerical quantum dynamics |
| [DodoVisionAI](https://github.com/diogommpires-glitch/dodovisionai-publication) | Experimental multimodal signal processing and presentation-attack detection |
| [PAD identity leakage](https://github.com/diogommpires-glitch/pad-identity-leakage-publication) | Identity-overlap and benchmark split audits |
| [SECOM Quality Lab](https://github.com/diogommpires-glitch/secom-quality-lab) | Semiconductor inspection prioritisation |
| [Dodo Mem](https://github.com/diogommpires-glitch/dodo-mem) | Evidence-linked memory and bounded retrieval |

The dashboard is a static snapshot checked on **12 November 2026**. Its eight projects are the repositories linked above; the profile repository and private activity are excluded. GitHub classifies 8,109,927 source bytes across nine languages in these projects. The chart shows those byte shares, not skill, effort or time spent. Its “Other” segment combines the six smaller language classifications.

The thirteen commits belong to the public snapshot histories. All thirteen have UTC commit dates of 12 November 2026. This is not a contribution calendar or a claim about daily working habits.

<details>
<summary>Dashboard data and portrait</summary>

The dated public metadata, project heads and language byte counts are saved in [data/public-metrics.json](data/public-metrics.json). To refresh the figures, collect the same public repository metadata, languages and complete commit histories, replace that JSON, then regenerate both layouts with Python 3.11 or later:

```sh
python scripts/generate_profile.py
```

The desktop and phone layouts are static SVGs containing text, shapes and an embedded copy of [the kitty portrait](assets/kitty.png). The portrait was adapted from my supplied photograph by removing its background. The original photograph is not included. There are no scripts, external image requests, font downloads or automatic publishing jobs.

</details>

Original work is available under the [PolyForm Noncommercial licence](LICENSE). See [LICENSING.md](LICENSING.md) for the scope and third-party terms.
