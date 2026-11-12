"""Architecture diagram of the Aeria platform (docs/architecture.svg)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture.svg"
INK, INK2, LINE, SURFACE = "#1f2328", "#57606a", "#8c959f", "#ffffff"
MOD = {1: "#2a78d6", 2: "#1baf7a", 3: "#eb6834", 4: "#6250d6", 5: "#d03b3b", 6: "#c98500", 7: "#57606a"}
W, H = 1240, 700

parts: list[str] = []


def box(x, y, w, h, title, sub="", module=None, fill="#f6f8fa", dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    stroke = MOD[module] if module else LINE
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{dash}/>')
    ty = y + (h / 2 + 4 if not sub else 28)
    parts.append(f'<text x="{x + w / 2}" y="{ty}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{escape(title)}</text>')
    if sub:
        for i, line in enumerate(sub.split("\n")):
            parts.append(f'<text x="{x + w / 2}" y="{ty + 17 + i * 14}" font-size="11" text-anchor="middle" fill="{INK2}">{escape(line)}</text>')
    if module:
        # module number on the top-left corner, half outside the box: never on the title
        parts.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{MOD[module]}" stroke="#fff" stroke-width="2"/>'
                     f'<text x="{x}" y="{y + 4}" font-size="10" font-weight="700" text-anchor="middle" fill="#fff">{module}</text>')


def arrow(x1, y1, x2, y2, label="", dy=-6, color=INK2, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#a)"{dash}/>')
    if label:
        parts.append(f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 + dy}" font-size="10.5" text-anchor="middle" fill="{INK2}">{escape(label)}</text>')


def zone(x, y, w, h, title, module):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{MOD[module]}" '
                 f'stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="2 4"/>')
    parts.append(f'<text x="{x + 12}" y="{y + 18}" font-size="12" font-weight="700" fill="{MOD[module]}">{escape(title)}</text>')


# ---------------------------------------------------------------- layout
zone(20, 50, 470, 200, "Module 1 · capteurs IoT", 1)
box(40, 80, 130, 64, "Capteurs ESP32", "SDS011 / SPS30, NO₂, O₃\n6 au Havre", 1)
box(200, 80, 120, 64, "Mosquitto", "MQTT QoS 1\nACL par capteur", 1)
box(350, 80, 120, 64, "Ingestion", "Spring Boot\nvalidation, dédoublonnage", 1)
box(200, 170, 270, 56, "PostgreSQL opérationnel", "mesures, santé des capteurs", 1)
arrow(170, 112, 200, 112, "MQTT")
arrow(320, 112, 350, 112)
arrow(410, 144, 380, 170)

zone(20, 280, 470, 170, "Module 2 · pipeline de données", 2)
box(40, 316, 150, 56, "Open data LCSQA", "data.gouv.fr, horaire", 2, fill=SURFACE)
box(220, 316, 120, 56, "ETL pandas", "nettoyage, drapeaux\nindice ATMO", 2)
box(370, 316, 100, 56, "Entrepôt", "schéma en étoile\n902 607 valeurs", 2)
arrow(190, 344, 220, 344)
arrow(340, 344, 370, 344)
arrow(335, 226, 280, 316, "export", dy=0)

zone(520, 50, 330, 200, "Module 3 · prévision 24 h", 3)
box(540, 80, 140, 64, "Open-Meteo", "prévisions météo\némises la veille", 3, fill=SURFACE)
box(700, 80, 130, 64, "scikit-learn", "5 modèles\ngradient boosting", 3)
box(620, 170, 210, 56, "API FastAPI", "indice ATMO de demain", 3)
arrow(680, 112, 700, 112)
arrow(765, 144, 725, 170)
arrow(470, 330, 700, 140, "historique", dy=-4)

zone(520, 280, 330, 170, "Module 4 · back-office", 4)
box(540, 312, 290, 56, "Spring Boot + Thymeleaf", "parc, techniciens, tickets, interventions", 4)
box(540, 380, 290, 52, "PostgreSQL : règles de gestion", "triggers, contraintes d'exclusion, KPI", 4)
arrow(470, 210, 560, 312, "santé capteurs (API)", dy=-2, dashed=True)

zone(880, 50, 340, 400, "Module 6 · tableau de bord", 6)
box(900, 90, 300, 70, "Site React (GitHub Pages)", "carte Leaflet, graphiques, prévision\nétude UX, page de présentation", 6)
box(900, 200, 300, 56, "Instantané JSON", "export_data.py : entrepôt, prévision, parc", 6)
box(900, 300, 300, 120, "Public", "« l'air sera-t-il bon demain ? »", fill=SURFACE)
arrow(1050, 200, 1050, 160)
arrow(1050, 300, 1050, 160, dashed=True)
arrow(830, 198, 900, 228, "prévision", dy=-6)
arrow(830, 340, 900, 238, "parc", dy=10)

zone(20, 480, 1200, 100, "Module 5 · sécurité (transverse)", 5)
box(40, 510, 250, 52, "EBIOS RM", "5 ateliers, 5 risques, 13 mesures", 5)
box(310, 510, 270, 52, "Audit", "nmap, Varys, OSV, contrôles web", 5)
box(600, 510, 300, 52, "Wazuh", "15 règles : journaux back-office, ingestion, MQTT", 5)
box(920, 510, 280, 52, "ISO 27001:2022", "déclaration d'applicabilité (35)", 5)
arrow(750, 510, 690, 432, "journaux", dy=0, color=MOD[5], dashed=True)

zone(20, 600, 1200, 70, "Module 7 · vitrine et intégration continue", 7)
box(40, 618, 1160, 40, "GitHub Actions sur les 7 dépôts : tests (Java, Python, JS), PostgreSQL de service, Wazuh 4.14.9 jetable, axe-core, images Docker, déploiement Pages", fill=SURFACE)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'style="font-family:Segoe UI,Helvetica,Arial,sans-serif">'
       f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0 0 L10 5 L0 10 z" fill="{INK2}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
       f'<text x="20" y="32" font-size="18" font-weight="700" fill="{INK}">Aeria : architecture de la plateforme</text>'
       + "".join(parts) + "</svg>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print("wrote", OUT)
