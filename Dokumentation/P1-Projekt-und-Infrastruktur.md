# P1 – Projekt und Infrastruktur

**Gruppe 1 · M324 DevOps · 09.11.2026**

## Projekt und Umfang

Wir entwickeln ein Backend für die Flughafen- und Flugverwaltung. Der Flughafenservice erfasst Flughäfen und stellt eine Liste bereit. Der Flugservice erfasst Flüge und prüft Abflug- und Zielflughafen über die API des Flughafenservice. Die beiden Dienste sind eigenständig und verwenden jeweils ihre eigene Datenbank. Die erste Version umfasst die Issues [#1](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/1), [#2](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/2) und [#3](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/3).

## Technologieentscheid des Teams

| Bereich | Entscheid | Begründung |
| --- | --- | --- |
| Programmiersprache | Python für beide Dienste | Eine gemeinsame Sprache vereinfacht lokale Entwicklung, Reviews und Testautomatisierung. |
| REST-API | FastAPI | Typisierte Eingaben unterstützen die Validierung von Flughafenkürzeln, Kapazitäten und Flugzeiten. Die generierte OpenAPI-Dokumentation macht die Schnittstellen für beide Dienste nachvollziehbar. |
| Tests | pytest | Fixtures und Parametrisierung eignen sich für wiederholbare Erfolgs- und Fehlerfälle. FastAPI dokumentiert Endpoint-Tests mit pytest und TestClient. |
| Datenbank | PostgreSQL | Eindeutige Flughafenkürzel lassen sich per Datenbank-Constraint absichern. Für die lokale Entwicklung ist PostgreSQL im Container geplant, mit einer eigenen Datenbank und eigenen Zugriffsrechten pro Dienst. |
| CI/CD | GitHub Actions | Repository, Pull Requests und Pipeline-Läufe bleiben auf einer Plattform. P3 automatisiert Build und Tests, P3b publiziert versionierte Artefakte und P4 verwendet diese beim Deployment. |

## Projektorganisation und Zugriffe

- Das [GitHub-Repository](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1) enthält die Ordner `Theorie/`, `Dokumentation/` und `Code/`. Die [README](../README.md) ist der Einstieg in die Unterlagen.
- Das [Kanban-Board](https://github.com/users/SilvanHahnTBZ/projects/1/views/1) enthält Todo, In Progress, Review, Done und Backlog. Die Aufgaben für spätere Modultage liegen im Backlog.
- Die Gruppe erfasst ihren Aufwand pro Person, Modultag und Aufgabe im [Zeitlog](https://docs.google.com/spreadsheets/d/12KcGT1z2t_Fag7OSbxu6rCZNN7VGnC3hw1QQB_7yJAM/edit). Laut Bestätigung aus der Gruppe ist der Schreibzugriff für die Lehrperson dort erteilt.
- Die Lehrperson hat die GitHub-Einladung angenommen und besitzt als Mitwirkende Schreibzugriff auf das Repository. Der Zugriff wurde am 09.11.2026 in GitHub geprüft.

## KI-Nachweis

- **Eigener Ausgangspunkt** – Das Team hatte das Flughafenprojekt gewählt und Repository, Board und Zeitlog eingerichtet. Die Technologiewahl war offen.
- **Tool und Prompt** – ChatGPT Work. Kurzfassung des Prompts: P1 für das Flughafenprojekt fertigstellen, offene Entscheidungen einzeln abfragen und passende Optionen vorschlagen.
- **Verglichene Varianten** – Python oder Java/Kotlin/TypeScript, FastAPI oder Flask, pytest oder unittest, PostgreSQL oder SQLite sowie GitHub Actions oder GitLab CI/CD. Flask bietet einen schlanken Einstieg, erfordert für dieses Projekt aber zusätzliche Arbeit für Validierung und API-Dokumentation. SQLite vereinfacht den lokalen Start. PostgreSQL passt zur vorgesehenen getrennten Datenhaltung der Dienste und zum späteren Deployment.
- **Prüfung** – Den P1-Auftrag und die Flughafen-Storys mit der offiziellen Dokumentation zu Validierung, Tests, Datenbankregeln und GitHub Actions abgeglichen. Risiken für P2 bis P4 sind die Erreichbarkeit der Flughafen-API, die Trennung der Datenbankzugriffe und der Umgang mit Pipeline-Secrets. Die Umsetzung wird in diesen Praxisaufträgen überprüft.
- **Eigene Entscheidung** – Das Team hat Python, FastAPI, pytest, PostgreSQL und GitHub Actions bestätigt. Für die Testdokumentation klären wir mit der Lehrperson, wie die in P2 genannte JavaDoc-Syntax auf Python-Docstrings übertragen werden soll.

## Quellen

- [TBZ P1 – Projekt-Setup und Infrastruktur](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Projekt/P1_Praxis_Infrastruktur.md)
- [TBZ Flughafenprojekt – User Stories und Schnittstellen](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Projekt/Projekt1_Fl%C3%BCge.md)
- [TBZ P2 – Anwendung v1 und Unit Tests](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Projekt/P2_Praxis_App_v1.md)
- [FastAPI-Funktionen](https://fastapi.tiangolo.com/features/) · [FastAPI-Tests](https://fastapi.tiangolo.com/tutorial/testing/) · [Flask](https://flask.palletsprojects.com/en/stable/) · [pytest](https://docs.pytest.org/en/stable/getting-started.html)
- [PostgreSQL-Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) · [SQLite-Einsatzgebiete](https://www.sqlite.org/whentouse.html) · [GitHub Actions für Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
