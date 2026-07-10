# INFECTED ORIGINS — V4-Bildbibel: Figuren

Stand: 10. Juli 2026. Diese Datei ersetzt die V3-Prompts vollständig.

## Verbindlicher Look

- photorealistischer Live-Action-Film, zeitgenössisches Deutschland
- geerdeter Medical-Thriller, keine futuristische Glaskathedrale
- natürliche, unretuschierte Haut; reale Stoffe und Gebrauchsgegenstände
- zurückhaltendes 35-mm-Korn, praktische Lichtquellen, gedämpfte Cyan-/Amber-Palette
- Figurenmaster exakt **4:5**
- keine Schrift, Logos, Wasserzeichen, Beauty-Retusche oder Identitätsmischung
- schwarze Fäden sind dünn und subdermal; A0,6 bleibt lokal, A0,8 wandert systemisch

## Referenzhierarchie

1. Hauptfilm-Frames sperren Identität, Kostüm, Raum und Props.
2. Ein akzeptierter V4-Master sperrt jede spätere Zustandsvariante.
3. Stilreferenzen dürfen niemals Gesicht oder Körperform überschreiben.

Hauptfilm-Frames liegen unter `assets/references/main-film/`. Sie sind Referenzmaterial, keine öffentlichen Galerie-Assets.

## Finale Figurenprompts

### Richard Voss — vor der Infektion

**Ausgabe:** `assets/v4/characters/richard.png`
**Referenz:** `assets/characters/richard-akt-i.png`

```text
Identity-preserving 4:5 portrait of Dr. Richard Voss, 52, same face, hairline,
glasses and build as the supplied reference. Warm cramped basement lab, rumpled shirt
and worn cardigan, exhausted but still hopeful. Photorealistic live-action German
medical thriller, natural skin, practical tungsten light, restrained 35mm grain;
no infection, text, logo, watermark, glamour or redesign.
```

### Richard Voss — A0,8

**Ausgabe:** `assets/v4/characters/richard-infected.png`
**Referenz:** `assets/v4/characters/richard.png`

```text
Preserve Richard's identity exactly. Same man in a plain white lab coat under cold
institutional light; pale, sweating, with thin black subdermal threads moving from
wrist over elbow toward neck. 4:5 live-action portrait, controlled body horror,
no gore, tentacles, facial redesign, text, logo or watermark.
```

### Eva Voss

**Ausgabe:** `assets/v4/characters/eva.png`
**Referenz:** `assets/characters/eva.png`

```text
Identity-preserving 4:5 portrait of Eva Voss, 53, terminally ill but lucid and
autonomous, in her modest warm kitchen. Preserve her exact face and age; frail body,
soft cardigan, direct attentive gaze. Natural tungsten and rainy window light,
photorealistic 35mm drama; no hospital glamour, text, logo or watermark.
```

### Nora Voss

**Ausgabe:** `assets/v4/characters/nora.png`
**Referenzen:** `lilith-face.png`, `lilith-field.png`

```text
Strict identity reconstruction from the supplied Lilith film frames: Dr. Nora Voss,
28, before becoming Lilith. Same face, ears, hairline and proportions, dark hair tied
back, ordinary rain jacket, warm domestic threshold, alert molecular-biologist gaze.
4:5 photorealistic live-action portrait, natural skin and fine grain; no white coat,
infection, text, logo, watermark or redesign.
```

### Lilith

**Ausgabe:** `assets/v4/characters/lilith.png`
**Referenzen:** `assets/v4/characters/nora.png`, `lilith-face.png`, `lilith-field.png`

```text
Identity-preserving transformation of Nora into Lilith: unquestionably the same
woman, same facial geometry and age. Low bun, plain white main-film coat, cool tiled
lab light, one thin local black line below the elbow only. 4:5 photorealistic portrait,
restrained 35mm grain; no full-body infection, new face, text, logo or watermark.
```

### Kessler

**Ausgabe:** `assets/v4/characters/kessler.png`
**Referenz:** `assets/characters/kessler.png`

```text
Identity-preserving 4:5 portrait of Kessler, 61, in a dark overcoat at an almost empty
railway-station café. Friendly, precise, unreadable; ordinary contemporary wardrobe,
rain and practical fluorescent/tungsten mix. Photorealistic 35mm thriller; no villain
caricature, corporate logo, text or watermark.
```

### Klara

**Ausgabe:** `assets/v4/characters/klara.png`
**Referenzen:** `klara-face.png`, `klara-lab.png`

```text
Strict identity-preserving 4:5 portrait of the 18-year-old Klara from the supplied
film frames. Same brown hair, face, earrings and pearl necklace, at home before the
abduction, awake neutral expression, warm window light. She is a young adult, never a
child. Photorealistic live action; no hospital gown, infection, text or watermark.
```

### Dr. Susan

**Ausgabe:** `assets/v4/characters/susan.png`
**Referenz:** `susan-lab.png` — ausschließlich die maskierte Person rechts mit Tablet

```text
Strict costume- and identity-preserving 4:5 portrait of Susan, the masked clinician on
the RIGHT of the reference. Preserve visible eyes, brow, short dark hair, white coat,
pale surgical mask and tablet; modest grey-tiled holding room and cold practical light.
Ignore Lia on the left. No unmasking, identity blend, text, logo or watermark.
```

### Lia

**Ausgabe:** `assets/v4/characters/lia.png`
**Referenzen:** `lia-face.png`, `lia-credit.png`, `susan-lab.png` für die Uniform links

```text
Strict identity-preserving 4:5 portrait of Lia from the supplied face frames. Neutral
attentive expression, dark hair pulled back, exact white short-sleeved nursing tunic
with purple trim and a small practical key ring. Grey tiled room, natural skin, muted
cyan grade. Do not borrow Susan's face, coat, mask or tablet; no text or watermark.
```

### Frank

**Ausgabe:** `assets/v4/characters/frank.png`
**Referenzen:** `frank-face.png`, `frank-field.png`

```text
Identity-preserving 4:5 portrait of adult Frank from the supplied main-film frames.
Same lean build, very short hair and face, awake in a plain hospital gown inside the
modest cold holding room, frightened but not yet infected. Photorealistic 35mm realism;
no restraints emphasized, no black veins, text, logo or watermark.
```

### Sicherheit

**Ausgabe:** `assets/v4/characters/security.png`
**Referenzen:** `guards-field.png`, `white-van.png`

```text
4:5 ensemble portrait of exactly the two adult male GenetiX guards from the main-film
reference: preserve the smaller man on the left and the taller broad-built man on the
right, understated black tactical clothing, radios and practical flashlights, beside a
light silver-grey unmarked MPV on a wet forest road. Contemporary and plausible, not
military spectacle; no women, logos, badges, sci-fi armor, text or watermark.
```

## Ausschlüsse aus V3

- kein Vorstand und kein Vorstandsportrait
- keine 22-jährige Nora; sie ist 28
- keine kindliche Klara; sie ist 18 und die Hauptfilmfigur
- kein weißer Cargo-Transporter; der Film-Prop ist ein heller silbergrauer MPV
- kein generisches grünes Sci-Fi-Labor
