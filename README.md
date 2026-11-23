
# DevOps – Gruppenprojekt

## Projektbeschreibung

Dieses Repository enthält unser Gruppenprojekt im Modul DevOps.

Ziel ist die Entwicklung einer Backend-Anwendung mit einer REST-API sowie die praktische Anwendung von DevOps-Methoden wie Versionsverwaltung, Testing, CI/CD und agiler Zusammenarbeit.

**Projekt:** Flughafen- und Flugverwaltung  
**Teamgrösse:** 4 Personen  
**Technologien:** Python, FastAPI, pytest, PostgreSQL und GitHub Actions

---

## Projektstruktur

Das Repository ist folgendermassen aufgebaut:

- [Theorie](Theorie/) – Theorieinhalte und Lernaufträge
- [Dokumentation](Dokumentation/) – Projektdokumentation, Architektur und technische Entscheidungen
- [Code](Code/) – Quellcode, Konfigurationen und Tests

## Theorieinhalte

In diesem Verzeichnis werden die bearbeiteten Theorieblöcke als Markdown-Dateien dokumentiert.

Alle erstellten Theoriedateien werden hier direkt verlinkt.

- [T1 – DevOps-Kultur: CALMS und The Three Ways](Theorie/T1_DevOps_Kultur.md)
- [T2 – DevOps Prozesse: SDLC, DevOps Lifecycle und MVP](Theorie/T2_DevOps_Prozesse.md)
- [T3 – Continuous Integration und Versionsstrategien](Theorie/T3_Continuous_Integration.md)
- [T4 – Continuous Delivery, Continuous Deployment und Betriebsrisiken](Theorie/T4_Continuous_Deployment.md)

## Dokumentation

Hier befinden sich die Dokumentationen zu unserem Projekt.

- [P1 – Projekt und Infrastruktur](Dokumentation/P1-Projekt-und-Infrastruktur.md) mit Technologieentscheid und KI-Nachweis
- [P2 – Applikation v1 mit Unit Tests](Dokumentation/P2-Applikation-v1.md): Architektur, Endpoints, Fehlerfälle, Testkonzept und KI-Nachweis

Code:

- [Flughafenservice](Code/airport-service/README.md) – US-01 und US-02
- [Flugservice](Code/flight-service/README.md) – US-03

Geplante Themen:

- Projektbeschreibung und Anforderungen
- Technologie- und Infrastrukturentscheidungen
- Architektur und Datenbank
- Git- und Branching-Strategie
- Testing und Qualitätssicherung
- CI/CD-Pipeline
- KI-Nachweis und Variantenvergleich

Alle erstellten Dokumentationsdateien werden hier direkt verlinkt.

## Projektmanagement

### Kanban-Board

[GitHub Kanban-Board](https://github.com/users/SilvanHahnTBZ/projects/1)

Unser Kanban-Board verwendet folgende Phasen:

- **To Do** – Geplante Aufgaben
- **In Progress** – Aufgaben in Bearbeitung
- **Review** – Aufgaben zur Überprüfung
- **Done** – Abgeschlossene Aufgaben
- **Backlog** – Aufgaben für spätere Modultage

### Zeitlogging

[Zeitlogging öffnen](https://docs.google.com/spreadsheets/d/12KcGT1z2t_Fag7OSbxu6rCZNN7VGnC3hw1QQB_7yJAM/edit?usp=sharing)

Jedes Gruppenmitglied dokumentiert die aufgewendete Zeit pro Modultag und Aufgabe.

Erfasst werden:

- Datum
- Gruppenmitglied
- Aufgabe
- Zeitaufwand
- Beschreibung der Tätigkeit

## Persönliche Lernjournale (freiwillig)

Persönliche Lernjournale können separat geführt werden.

- Lernjournal Silvan: [M324 DevOps – Persönliches Lernjournal – Silvan Hahn](https://docs.google.com/document/d/1YfETWUD9T1VkooYqIDxbH_vE80vJdmgc3RXRgZFIFKk/edit?tab=t.0)
- Lernjournal Ricardo: [Lernjournal Ricardo Kraus](https://docs.google.com/document/d/1DGdcHLWD9LtrQmbclRaXGcRknNY7jJQQkrzMefetWHA/edit?usp=sharing)
- Lernjournal Mitglied 3: Link folgt
- Lernjournal Mitglied 4: Link folgt

## Technologien

Beide Mikroservices verwenden denselben Technologie-Stack.

| Bereich | Technologie |
|---------|-------------|
| Programmiersprache | Python |
| Backend-Framework | FastAPI |
| Unit-Tests | pytest |
| Datenbank | PostgreSQL |
| Versionsverwaltung | Git / GitHub |
| CI/CD | GitHub Actions |
| Projektmanagement | GitHub Projects |

## Zusammenarbeit

Das Projekt wird von vier Gruppenmitgliedern gemeinsam bearbeitet.

Die Zusammenarbeit erfolgt über GitHub mit folgenden Grundsätzen:

- Aufgaben werden im Kanban-Board verwaltet.
- Änderungen werden durch Git-Commits dokumentiert.
- Neue Funktionen werden nach der vereinbarten Branching-Strategie entwickelt.
- Code wird vor dem Zusammenführen überprüft.
- Die Lehrperson erhält Schreibrechte auf das Repository und das Zeitlogging.

## CI/CD

Im Verlauf des Projekts wird eine CI/CD-Pipeline implementiert.

Geplante Funktionen:

- Automatische Ausführung von Tests
- Überprüfung der Codequalität
- Automatisierte Build-Prozesse
- Optionales Deployment

## KI-Nutzung

KI wird als Unterstützung für Variantenvergleiche, Risikoanalysen und technische Fragestellungen eingesetzt.

Die endgültigen Projekt- und Technologieentscheidungen werden vom Team getroffen und begründet.

Mindestens ein KI-gestützter Variantenvergleich wird mit Prompt, KI-Hinweisen, geprüften Risiken und eigener Entscheidung dokumentiert.
