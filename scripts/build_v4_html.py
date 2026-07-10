#!/usr/bin/env python3
"""Build the semantic V4 screenplay HTML from the canonical Markdown source."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "screenplay" / "infected-origins-v4.md"
TARGET = ROOT / "screenplay" / "infected-origins-v4.html"


@dataclass
class Scene:
    number: int
    slug: str
    lines: list[str] = field(default_factory=list)


@dataclass
class Act:
    source_title: str
    html_id: str
    label: str
    beat: str
    scenes: list[Scene] = field(default_factory=list)


ACT_META = {
    "PROLOG": ("prolog", "Prolog", "Das Geständnis"),
    "I — LIEBE": ("act-1", "I — Liebe", "Eine Grenze wird versprochen"),
    "II — KORRUPTION": ("act-2", "II — Korruption", "Aus Hoffnung wird ein Verfahren"),
    "III — VERERBUNG": ("act-3", "III — Vererbung", "Nora trifft die eigene Entscheidung"),
    "EPILOG — ÜBERGABE AN „INFECTED“": (
        "epilogue",
        "Epilog — Übergabe an „INFECTED“",
        "Die Konsequenz erreicht Klara",
    ),
}


STILLS = {
    0: [
        (
            "scene-00-kassette",
            "scene-00-kassette.png",
            1830,
            766,
            "Richard zeichnet nachts im warmen Kellerlabor sein Geständnis auf; Kassette und zwei Kurven liegen zwischen ihm und der Kamera.",
            "Eintrag 47: Richard kennt den Unterschied zwischen schneller Wirkung und Kontrolle.",
        )
    ],
    1: [
        (
            "scene-01-grenze",
            "scene-01-grenze.png",
            1920,
            804,
            "Eva und Nora sitzen einander in der warmen Küche gegenüber; zwischen ihren Händen liegt das alte Foto vom Meer.",
            "Evas Grenze ist eindeutig: ihr Körper, kein fremder.",
        )
    ],
    2: [
        (
            "scene-02-zwei-kurven",
            "scene-02-zwei-kurven.png",
            1934,
            810,
            "Richard und Nora betrachten im selben warmen Kellerlabor zwei gegensätzliche Kurven auf einem Monitor: schnell und toxisch, langsam und kontrolliert.",
            "A0,8 wirkt schnell. A0,6 bleibt länger kontrollierbar.",
        )
    ],
    5: [
        (
            "scene-05-pakt",
            "scene-05-pakt.png",
            1936,
            810,
            "Richard und Kessler sitzen sich tagsüber im verregneten Bahnhofscafé gegenüber; Karte, Akte und Evas Meerfoto liegen unberührt auf dem Tisch.",
            "Kessler verkauft Zeit — und macht aus Richards Ausnahme ein System.",
        )
    ],
    7: [
        (
            "scene-07-erste-luege",
            "scene-07-erste-luege.png",
            1932,
            808,
            "Nora sitzt im GenetiX-Tierlabor vor Transferdaten und einer schwarzen Gefäßstruktur; Richard und Kessler beobachten, wie sie den Befund als Ausreißer markiert.",
            "Noras erste Lüge ist klein genug, um vernünftig zu wirken.",
        )
    ],
    8: [
        (
            "scene-08-klara",
            "scene-08-klara.png",
            1938,
            810,
            "Der infizierte Richard zeigt den schwarzen Faden an seinem Arm, während Kessler Klaras Foto in einer offenen Akte präsentiert.",
            "Aus einer Prozentzahl wird ein Name: Klara.",
        )
    ],
    9: [
        (
            "scene-09-evas-wahl",
            "scene-09-evas-wahl.png",
            1934,
            808,
            "Eva und Richard halten gemeinsam die Einwilligung; an Richards Hand ist der schwarze Faden sichtbar, eine versiegelte Spritze liegt unbenutzt auf dem Beistelltisch.",
            "Eva stimmt nur für ihren eigenen Körper zu.",
        )
    ],
    10: [
        (
            "scene-10-notruf",
            "scene-10-notruf.png",
            1930,
            808,
            "Nora telefoniert neben der verstorbenen Eva mit dem Notruf; Einwilligung und leere Spritze liegen noch auf dem Nachttisch.",
            "Der Notruf macht aus Richards Entscheidung eine Spur — und aus Nora eine Mitwisserin.",
        )
    ],
    12: [
        (
            "scene-12-zusammenbruch",
            "scene-12-zusammenbruch.png",
            1934,
            810,
            "Richard liegt mit schwarzen Fäden im GenetiX-Flur, während Nora neben ihm kniet und den internen medizinischen Alarm auslöst.",
            "Richard bricht beim Versuch zusammen, Klara zu stoppen.",
        )
    ],
    13: [
        (
            "scene-13-a06",
            "scene-13-a06.png",
            1934,
            808,
            "Nora untersucht im Morgengrauen einen einzelnen lokalen schwarzen Faden an ihrem Arm und protokolliert getrennte Kontaktproben.",
            "A0,6 ist kontrolliert — ausdrücklich nicht sicher.",
        )
    ],
    14: [
        (
            "scene-14-lilith",
            "scene-14-lilith.png",
            1934,
            808,
            "Lilith sitzt im weißen Kittel vor Klaras Porträt und klaren Symbolen für Transport stoppen oder freigeben; Meerfoto und Datenträger liegen neben ihrer Hand.",
            "Nora kennt die Alternative und autorisiert den Transport selbst.",
        )
    ],
    15: [
        (
            "scene-15-labor",
            "scene-15-labor.png",
            1930,
            808,
            "Lia und die maskierte Susan stehen im gekachelten Labor an zwei getrennten Sets; Frank wartet sichtbar hinter der Scheibe, Lilith geht.",
            "Die Übergabe an den Hauptfilm: Susan, Lia und Frank sind bereits an ihren Positionen.",
        ),
        (
            "scene-15-van",
            "scene-15-van.png",
            1934,
            808,
            "Zwei männliche Sicherheitskräfte stehen neben einem hellen unmarkierten Van vor Klaras dunklem Haus; Klara beobachtet sie aus dem warmen Fenster.",
            "Der Van hält vor Klaras Haus — unmittelbar vor „INFECTED“.",
        ),
    ],
}


CUES = {
    "RICHARD",
    "RICHARD (V.O.)",
    "NORA",
    "EVA",
    "EVA (V.O.)",
    "KESSLER",
    "LILITH",
    "SUSAN",
    "LIA",
    "FRANK",
    "PRÜFER",
    "PRÜFERIN",
    "STIMME AM TELEFON",
    "FAHRER (V.O.)",
}


def inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    return escaped


def section_lines(lines: list[str], heading: str) -> list[str]:
    start = lines.index(heading) + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return [line for line in lines[start:end] if line.strip() and line.strip() != "---"]


def parse_source(lines: list[str]) -> tuple[str, list[str], list[str], list[Act], list[str]]:
    logline = " ".join(section_lines(lines, "## Logline"))
    cast = [line[2:] for line in section_lines(lines, "## Figuren") if line.startswith("- ")]
    canon = [re.sub(r"^\d+\.\s+", "", line) for line in section_lines(lines, "## Kanonregeln des Compounds") if re.match(r"^\d+\.\s+", line)]
    handoff = [line[2:] for line in section_lines(lines, "## Kanonischer Übergabepunkt") if line.startswith("- ")]

    acts: list[Act] = []
    current_act: Act | None = None
    current_scene: Scene | None = None
    scene_re = re.compile(r"^###\s+(\d+)\.\s+(.+)$")

    for raw in lines:
        if raw.startswith("## "):
            title = raw[3:].strip()
            if title in ACT_META:
                html_id, label, beat = ACT_META[title]
                current_act = Act(title, html_id, label, beat)
                acts.append(current_act)
                current_scene = None
            elif title == "ENDE":
                current_act = None
                current_scene = None
            continue

        match = scene_re.match(raw)
        if match and current_act is not None:
            current_scene = Scene(int(match.group(1)), match.group(2).strip())
            current_act.scenes.append(current_scene)
            continue

        if current_scene is not None:
            current_scene.lines.append(raw)

    return logline, cast, canon, acts, handoff


def render_body(lines: list[str]) -> str:
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line or line == "---":
            continue

        cue_match = re.fullmatch(r"\*\*(.+?)\*\*", line)
        if cue_match and cue_match.group(1) in CUES:
            cue = cue_match.group(1)
            cue_html = inline_markdown(cue)
            output.append(f'<div class="dialogue"><p class="cue">{cue_html}</p>')
            dialogue_parts: list[str] = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not candidate:
                    index += 1
                    break
                if candidate.startswith("**") or candidate == "---":
                    break
                dialogue_parts.append(candidate)
                index += 1
            if dialogue_parts:
                output.append(f'<p class="line">{inline_markdown(" ".join(dialogue_parts))}</p>')
            output.append("</div>")
            continue

        if line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            output.append(f'<p class="dir em">{inline_markdown(line[1:-1])}</p>')
            continue

        if cue_match:
            output.append(f'<p class="dir em"><strong>{html.escape(cue_match.group(1))}</strong></p>')
            continue

        paragraph = [line]
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate:
                index += 1
                break
            if candidate == "---" or candidate.startswith("**"):
                break
            paragraph.append(candidate)
            index += 1
        output.append(f'<p class="dir">{inline_markdown(" ".join(paragraph))}</p>')

    return "\n".join(output)


def render_picture(scene_number: int, still: tuple[str, str, int, int, str, str]) -> str:
    anchor, filename, width, height, alt, caption = still
    loading = "eager" if scene_number == 0 else "lazy"
    priority = ' fetchpriority="high"' if scene_number == 0 else ""
    stem = filename.removesuffix(".png")
    return f"""
<figure class="scene-image">
  <a href="../bilder.html#still-{anchor}" aria-label="Dieses Bild in der Galerie öffnen">
    <picture>
      <source srcset="../assets/v4/stills/{stem}.webp" type="image/webp">
      <img src="../assets/v4/stills/{filename}" width="{width}" height="{height}" loading="{loading}" decoding="async"{priority} alt="{html.escape(alt, quote=True)}">
    </picture>
  </a>
  <figcaption>{html.escape(caption)}</figcaption>
</figure>""".strip()


def render_scene(scene: Scene, act_id: str) -> str:
    scene_id = f"scene-{scene.number:02d}"
    figures = "\n".join(render_picture(scene.number, still) for still in STILLS.get(scene.number, []))
    return f"""
<section class="scene" id="{scene_id}" data-scene data-act="{act_id}" aria-labelledby="{scene_id}-title">
  <h3 class="slug" id="{scene_id}-title"><span class="scene__number">{scene.number}.</span> {html.escape(scene.slug)}</h3>
{figures}
  {render_body(scene.lines)}
</section>""".strip()


def render_nav(acts: list[Act]) -> str:
    groups: list[str] = []
    for act in acts:
        scene_links = "\n".join(
            f'<li><a href="#scene-{scene.number:02d}" data-scene-link>{scene.number}. {html.escape(scene.slug)}</a></li>'
            for scene in act.scenes
        )
        groups.append(
            f"""<li>
  <a class="act" href="#{act.html_id}" data-act-link>{html.escape(act.label)}</a>
  <ol>{scene_links}</ol>
</li>"""
        )
    return "\n".join(groups)


def render_details(title: str, items: list[str], *, ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    list_items = "\n".join(f"<li>{inline_markdown(item)}</li>" for item in items)
    return f"""
<details class="dramatis-personae">
  <summary>{html.escape(title)}</summary>
  <{tag}>
    {list_items}
  </{tag}>
</details>""".strip()


def build() -> str:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    logline, cast, canon, acts, handoff = parse_source(lines)
    nav = render_nav(acts)
    act_sections = []
    for act in acts:
        scenes = "\n".join(render_scene(scene, act.html_id) for scene in act.scenes)
        act_sections.append(
            f"""
<section class="act-block" id="{act.html_id}" aria-labelledby="{act.html_id}-title">
  <header class="act-divider">
    <p>{html.escape(act.beat)}</p>
    <h2 id="{act.html_id}-title">{html.escape(act.label)}</h2>
  </header>
  {scenes}
</section>""".strip()
        )

    cast_details = render_details("Figuren", cast)
    canon_details = render_details("Kanonregeln des Compounds", canon, ordered=True)
    handoff_details = render_details("Kanonischer Übergabepunkt zum Hauptfilm", handoff)

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="INFECTED ORIGINS — Drehbuch v4. Ein vollständig überarbeitetes Prequel zu INFECTED.">
  <meta name="theme-color" content="#080a0d">
  <title>INFECTED ORIGINS — Drehbuch v4</title>
  <link rel="stylesheet" href="../assets/site/origins-v4.css">
  <script src="../assets/site/origins-v4.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#screenplay-content">Direkt zum Drehbuch</a>

  <header class="site-header">
    <div class="site-header__inner">
      <a class="site-brand" href="../index.html">Infected <span>Origins</span></a>
      <nav class="site-nav" aria-label="Hauptnavigation">
        <ul>
          <li><a href="../index.html">Start</a></li>
          <li><a href="infected-origins-v4.html" aria-current="page">Drehbuch</a></li>
          <li><a href="../bilder.html">Bilder</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <progress class="reading-progress" data-reading-progress max="100" value="0"><span class="visually-hidden">Lesefortschritt</span></progress>

  <div class="reader-layout">
    <aside class="scene-nav" id="scene-navigation" data-scene-nav aria-label="Szenennavigation">
      <h2 class="scene-nav__title" data-scene-nav-title>Szenen</h2>
      <ol>{nav}</ol>
    </aside>
    <button class="scene-nav-scrim" data-scene-nav-scrim aria-label="Szenennavigation schließen"></button>
    <button class="scene-nav-toggle" data-scene-nav-toggle data-label-open="Szenen öffnen" data-label-close="Szenen schließen">Szenen</button>

    <main class="screenplay-main" id="screenplay-content" data-drawer-inert>
      <div class="screenplay-wrap">
        <section class="screenplay-cover" aria-labelledby="screenplay-title">
          <p class="kicker">Prequel zu „INFECTED“</p>
          <h1 id="screenplay-title">INFECTED ORIGINS</h1>
          <p class="screenplay-cover__subtitle">{inline_markdown(logline)}</p>
          <div class="screenplay-meta">
            <span>Drehbuch v4</span><span>10. Juli 2026</span><span>ca. 15–16 Minuten</span><span>16 Szenen</span>
          </div>
          <div class="screenplay-actions">
            <a class="btn" href="infected-origins-v4.md">Markdown lesen</a>
            <a class="btn ghost" href="../bilder.html">Bildwelt ansehen</a>
          </div>
        </section>

        {cast_details}
        {canon_details}

        <article class="screenplay" data-screenplay>
          {''.join(act_sections)}

          <section class="screenplay-end" aria-labelledby="screenplay-end-title">
            <div>
              <p class="kicker">Unmittelbar vor der ersten Szene von „INFECTED“</p>
              <h2 class="screenplay-end__title" id="screenplay-end-title">Ende</h2>
            </div>
          </section>
        </article>

        {handoff_details}

        <div class="screenplay-actions">
          <a class="btn" href="../bilder.html#stills">Alle V4-Bilder</a>
          <a class="btn ghost" href="../index.html">Zur Startseite</a>
        </div>
      </div>
    </main>
  </div>

  <footer class="site-footer" data-drawer-inert>
    <div class="container">INFECTED ORIGINS · Drehbuch v4 · 16 Szenen · Anschlussfassung 2026</div>
  </footer>
</body>
</html>
"""


if __name__ == "__main__":
    TARGET.write_text(build(), encoding="utf-8", newline="\n")
    print(TARGET)
