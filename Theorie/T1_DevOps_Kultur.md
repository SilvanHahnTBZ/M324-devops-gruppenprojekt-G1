# T1 – DevOps-Kultur: CALMS und The Three Ways

**Name:** Silvan Hahn  
**Modul:** M324 – DevOps  
**Auftrag:** [T1 Theorie DevOps-Kultur](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Projekt/T1_Theorie_DevOps_Kultur.md)  
**Quellen:** [CALMS](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Kultur/CALMS.md), [The Three Ways](https://gitlab.com/ch-tbz-it/Stud/m324/-/blob/main/Kultur/TheThreeWays.md), Fallstudie TechNova Solutions

---

## 1. Verständnis CALMS

CALMS beschreibt, auf welchen **Säulen** eine DevOps-Organisation steht. Die Grundidee: Alle fünf Bereiche müssen zusammen wachsen. Wer nur einen Bereich ausbaut (z. B. nur Automatisierung), macht noch kein DevOps. Das Fundament ist die Kultur.

| Bereich | Erklärung in eigenen Worten | Wo sichtbar bei TechNova |
|---------|-----------------------------|--------------------------|
| **C – Culture** | Dev, Test und Ops arbeiten nicht gegeneinander, sondern verfolgen ein gemeinsames Ziel: funktionierende Software beim Kunden. Fehler werden akzeptiert und gemeinsam gelöst, statt jemanden zu beschuldigen. Auch das Management muss diese Haltung mittragen. | **Vorher:** Silos, Schuldzuweisungen bei Fehlern. **Nachher:** Workshops und Teambuilding, stabilere Zusammenarbeit zwischen Entwicklung und Betrieb. Die Geschäftsleitung hat die Transformation selbst angestossen. |
| **A – Automation** | Wiederkehrende, manuelle Arbeit (Tests, Builds, Deployments, Monitoring) wird automatisiert. Das macht schneller und weniger fehleranfällig. Wichtig: Automatisierung allein ist nicht DevOps – sonst automatisiert man nur die Fehler. | **Vorher:** Tests und Deployments manuell und fehleranfällig. **Nachher:** CI/CD-Pipeline eingeführt. |
| **L – Lean** | Alles weglassen, was keinen Mehrwert für den Kunden bringt (Waste), z. B. Wartezeiten, unnötige Übergaben. Dazu gehört kontinuierliche Verbesserung in kleinen Schritten. | **Vorher:** Features kamen erst nach 6+ Monaten zum Kunden (viel Wartezeit = Waste). **Nachher:** Kanban-Boards, kleinere Releases im Wochenrhythmus. |
| **M – Measurement** | Entscheidungen werden auf Basis von Zahlen getroffen, nicht nach Bauchgefühl. Typische Metriken: Lead Time (Anforderung bis live), Deployment-Frequenz, MTTR (Zeit bis ein Ausfall behoben ist). | TechNova misst Deployment-Frequenz, Lead Time und MTTR. Dadurch ist der Erfolg belegbar: von halbjährlichen auf wöchentliche Releases. |
| **S – Sharing** | Wissen, Probleme und Lösungen werden geteilt, damit niemand den gleichen Fehler zweimal macht. Das funktioniert nur, wenn man keine Angst hat, Fehler zuzugeben – Sharing hängt also stark mit Culture zusammen. | Wiki, interne Lernformate und Erfahrungsberichte. |

---

## 2. Verständnis The Three Ways

The Three Ways (Gene Kim) schauen weniger auf die Organisation als **auf den Arbeitsfluss**: Wie kommt eine Änderung vom Entwickler zum Kunden, und wie kommt die Rückmeldung zurück?

### First Way – Systems Thinking (Flow)

Man betrachtet den **ganzen Weg** einer Änderung von der Idee bis zum Kunden als ein System – nicht nur den eigenen Teil. Ziel ist ein schneller, reibungsloser Fluss von links (Dev/Business) nach rechts (Ops/Kunde). Mittel dazu: kleine Änderungen, Arbeit sichtbar machen (Kanban), WIP begrenzen, unnötige Übergaben und Genehmigungen entfernen, Flaschenhälse finden und automatisieren.

**Bei TechNova:** Vorher arbeiteten Entwicklung, Test und Betrieb isoliert und jede Übergabe war manuell – jeder optimierte nur seinen Teil. Mit Kanban-Boards wurde die Arbeit sichtbar, mit der CI/CD-Pipeline wurde der Weg zum Kunden automatisiert. Ergebnis: wöchentliche statt halbjährliche Releases.

### Second Way – Amplify Feedback Loops (Feedback)

Jetzt die **Gegenrichtung**: Rückmeldungen von Ops und Kunden sollen schnell und laufend zurück zu Dev fliessen. Je früher ein Fehler bemerkt wird, desto billiger ist er zu beheben. Deshalb: automatisierte Tests (schnellstes Feedback), häufige kleine Deployments, Reviews, Monitoring.

**Bei TechNova:** Vorher konnte Kundenfeedback nicht schnell umgesetzt werden, weil nur alle sechs Monate released wurde – die Feedbackschleife war ein halbes Jahr lang. Nachher kommt Feedback dank wöchentlicher Releases und automatisierter Tests in der Pipeline viel schneller zurück. Auch die Metriken (z. B. MTTR) sind eine Form von Feedback.

### Third Way – Continual Learning and Experimentation (Lernen)

Die Organisation lernt dauernd dazu. Fehler werden nicht versteckt oder einer Person angelastet, sondern als Lernchance gesehen und geteilt. Teams dürfen experimentieren, und das Management deckt das. Wiederkehrende Probleme werden nicht mit Workarounds umgangen, sondern an der Ursache gelöst.

**Bei TechNova:** Vorher Fingerpointing bei Fehlern (typisches Zeichen schlechter Fehlerkultur). Nachher Erfahrungsberichte, Wiki und interne Lernformate – Wissen wird organisationsweit geteilt. Die Workshops sind der Startpunkt für diesen Kulturwandel.

---

## 3. Vergleich

**Kurz gesagt:** CALMS beantwortet die Frage *„Was braucht eine Organisation für DevOps?“* (Bausteine). The Three Ways beantworten *„Wie soll die Arbeit fliessen und sich verbessern?“* (Prozess). Beide meinen oft dasselbe, schauen aber aus einem anderen Winkel.

| Gemeinsame Idee | CALMS-Bezug | Bezug zu The Three Ways | Beispiel aus der Fallstudie | Eigene Einschätzung |
|-----------------|-------------|-------------------------|-----------------------------|---------------------|
| Zusammenarbeit statt Silos | **Culture** | **First Way** (ganzes System statt Insellösungen), **Third Way** (keine Silos, keine Schuldzuweisungen) | Workshops, Teambuilding; Dev und Ops arbeiten stabiler zusammen | Wichtigste Gemeinsamkeit. Ohne diesen Punkt funktioniert nichts anderes nachhaltig. |
| Schneller Fluss von Änderungen | **Automation**, **Lean** | **First Way** (Flow, kleine Batches, Flaschenhälse entfernen) | CI/CD-Pipeline, Kanban, wöchentliche Releases | CALMS nennt das Werkzeug (Automation), Three Ways erklären, *warum* es wichtig ist (Flow). |
| Entscheiden mit Daten / Feedback | **Measurement** | **Second Way** (Feedback verstärken) | Deployment-Frequenz, Lead Time, MTTR; schnelleres Kundenfeedback | Metriken sind eigentlich eine Feedbackschleife fürs ganze System. Hier passen die Modelle sehr gut zusammen. |
| Aus Fehlern lernen, Wissen teilen | **Sharing**, Culture | **Third Way** (kontinuierliches Lernen, Experimente) | Wiki, Lernformate, Erfahrungsberichte | Der Third Way geht weiter als Sharing: Er verlangt auch aktives Experimentieren, nicht nur Dokumentieren. |
| Kontinuierliche Verbesserung | **Lean** | **Third Way**, teilweise **First Way** | Schrittweise Transformation über 18 Monate | Beide Modelle sehen DevOps als Weg, nicht als Ziel, das man einmal erreicht. |

**Unterschiede:**

- **Blickwinkel:** CALMS ist eher eine Checkliste für die Organisation (Kultur, Tools, Messung, Wissen). The Three Ways beschreiben eine Richtung bzw. Reihenfolge: zuerst Flow, dann Feedback, dann Lernen.
- **Automatisierung:** Bei CALMS ist sie eine eigene Säule. Bei The Three Ways ist sie nur ein Mittel, um Flow (First Way) und schnelles Feedback durch Tests (Second Way) zu erreichen.
- **Messen:** CALMS hat Measurement als eigenen Bereich. Bei The Three Ways steckt Messen indirekt im Feedback.
- **Experimentieren:** Der Third Way betont Experimente auf Live-Systemen stärker. Bei CALMS kommt das nur am Rand unter Lean vor.

---

## 4. Bewertung der Transformation

Meiner Meinung nach hatten diese zwei Veränderungen den grössten Nutzen:

### 1. Die Einführung der CI/CD-Pipeline

- **CALMS:** Das ist direkt *Automation*. Die manuellen, fehleranfälligen Tests und Deployments fallen weg.
- **Three Ways:** Die Pipeline verbessert den *First Way* (Änderungen fliessen ohne manuelle Übergaben zum Kunden) und den *Second Way* (automatisierte Tests geben sofort Feedback, ob etwas kaputt ist).
- **Begründung:** Ohne Pipeline wären wöchentliche Releases gar nicht möglich gewesen. Die Pipeline ist also die technische Voraussetzung für das Hauptergebnis (halbjährlich → wöchentlich) und damit auch für die bessere Kundenzufriedenheit.

### 2. Der Kulturwandel (Workshops, Teambuilding, Wissensaustausch)

- **CALMS:** *Culture* und *Sharing*. Die Silos und das Fingerpointing wurden aktiv angegangen.
- **Three Ways:** *Third Way* (Fehler als Lernchance statt Schuldzuweisung) und *First Way* (das ganze System sehen statt nur die eigene Abteilung).
- **Begründung:** Laut CALMS-Unterlagen gilt: Wer nur automatisiert, „automatisiert die Fehler durch“. Die Pipeline nützt nur etwas, wenn sich die Leute auch trauen, häufig zu deployen, und bei Problemen zusammenarbeiten statt sich zu beschuldigen. Ich sehe den Kulturwandel deshalb als das Fundament und die Pipeline als das wichtigste Werkzeug darauf.

**Warum nicht die Metriken?** Die Metriken sind wichtig, um den Erfolg zu belegen und weiter zu verbessern. Sie verändern aber nichts direkt – sie zeigen nur, ob die anderen Massnahmen wirken. Darum stehen sie bei mir an dritter Stelle.

---

## 5. Transfer

**Beispiel:** Mein Lehrbetrieb SIX, Abteilung Digital Assets.

**Ist-Situation:**

- Bei unseren Projekten läuft vieles schon nach DevOps-Prinzipien: Alles geht über Git-Repositories und Pipelines, es gibt automatisierte Tests und Tools, die Fehler und Vulnerabilities automatisch melden.
- *Automation* und der *Second Way* (Feedback) sind also schon gut abgedeckt.
- Das Problem: Manchmal dauern Dinge lange, weil Zugriffe (Accesses) fehlen oder nur bestimmte Personen die nötigen Berechtigungen haben. Dann muss man auf diese Personen warten, auch für Feedback.

**Am stärksten verbessert werden müsste:**

- **CALMS: Lean.** Das Warten auf andere Personen bringt keinen Mehrwert und ist damit „Waste“. Die Arbeit ist eigentlich bereit, steht aber still, weil man von anderen abhängig ist.
- **Three Ways: First Way (Systems Thinking).** Der Flow von der Arbeit bis zum Ergebnis wird durch diese Abhängigkeiten gebremst. Fehlende Berechtigungen sind ein typischer Flaschenhals im System. Laut Unterlage sollen solche Übergänge reduziert und z. B. die Bereitstellung von Zugängen sogar automatisiert werden.

**Massnahme:** Bessere Confluence-Seiten, auf denen klar steht, welche Accesses man für welche Aufgaben braucht und wen man dafür fragen muss. So kann man Zugriffe früh beantragen und muss nicht erst warten, wenn man schon blockiert ist.

**Eigene Einschätzung:** Dass nicht alle alle Berechtigungen haben, verstehe ich. Gerade bei SIX ist Sicherheit sehr wichtig. Trotzdem ist es mühsam, wenn man deswegen warten muss. Deshalb geht es nicht darum, allen mehr Rechte zu geben, sondern den Weg zu den Rechten transparenter und schneller zu machen.

---

## KI-Nachweis

| | |
|---|---|
| **Eingesetztes Tool** | Claude (Anthropic) in Claude Code |
| **Wofür** | Ausarbeitung der Aufgaben 1–4 als Entwurf, Abgleich mit den Unterrichtsunterlagen CALMS und The Three Ways, Erklärung der Inhalte |
| **Prompt (Auszug)** | „Löse T1 mit mir zussamen (CALMS und The Three Ways, Fallstudie TechNova) und erkläre mir, was gemacht wurde, damit ich es verstehe. schaue dir zuerst noch an was ich schon gemacht habe und frage mich am ende die fragen ob ich es verstanden habe damit wir es am ende abschliessend und pushen können.“ |
| **Eigener Anteil** | Transfer (Aufgabe 5) mit Beispiel aus meinem Lehrbetrieb, eigene Schlussfolgerung, Prüfung des KI-Hinweises |
| **KI-Hinweis (ausgewählt)** | Automation darf nicht mit DevOps gleichgesetzt werden – die CALMS-Unterlage warnt ausdrücklich davor („Fehler komplett durchautomatisieren“). Deshalb sollte bei Aufgabe 4 nicht nur die Pipeline, sondern auch der Kulturwandel stehen. |
| **Geprüft mit** | CALMS.md, Abschnitt „A für Automation“: Die Aussage steht so in der Unterlage. |
| **Eigene Schlussfolgerung** | Der Auftrag war spannend und ich habe neue Sachen gelernt. Von CALMS und The Three Ways hatte ich vorher noch nichts gehört. Die KI hat mir geholfen, die Theorie zu verstehen und auf die Fallstudie anzuwenden. Beim Transfer habe ich gemerkt, dass bei SIX vieles schon automatisiert ist und das grössere Problem eher beim Flow (Wartezeiten wegen Berechtigungen) liegt. |
