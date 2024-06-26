# chainreport-converter
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.md)
[![de](https://img.shields.io/badge/lang-de-green.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.de.md)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/defb99bf113c42569e424afb71ba57da)](https://app.codacy.com/gh/nacrul-eth/chainreport-converter/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Konverter Tool für <https://chain.report/> in Zusammenarbeit mit <https://kryptowoelfe.de/>

## Verwendung
Es gibt als offizielle Release eine Windows Applikation (.exe / https://github.com/nacrul-eth/chainreport-converter/releases), welche auch unter Linux läuft (vorausgesetzt python3, kivy und MyPDF2 sind installiert). 

![grafik](https://github.com/nacrul-eth/chainreport-converter/assets/145897591/854117f9-0a94-4e35-8b91-5351e1a0cb1e)

 
Alternativ kann eine chainreport CSV-Datei erzeugt werden mit dem folgenden Befehl:

    python3 src/chainreport-converter.py "exchange type" "input-file" "output-file"
    => python3 src/chainreport_converter_script.py Hi-PDF hi-statement.csv chainreport.csv

## Aktuell unterstützte Platformen
Aktuell werden die folgenden Exchanges/Blockchains unterstützt:

- Hi-CSV (<https://hi.com>): Original, but limited version (No withdraw amounts in the Hi statement)
- Hi-PDF (<https://hi.com>): New, PDF based version with all transactions supported
- Plutus (<https://plutus.it>) (Rewards export only)

Für weitere Blockchain/Exchange Anbindungen bitte ein github-Ticket öffnen oder im Kryptwölfe Telegram nachfragen:

[@Krypto_Woelfe](https://t.me/kryptowoelfe)

## Entwicklung
Für pull request und um die Enwticklungsumgebung aufzusetzen bitte die requirements.txt Datei verwenden. Zusätzlich wird die Verwendung einer Python venv Umgebung empfohlen, um ungewollte Nebeneffekte zu vermeiden:

    python3 -m venv "VENV-FOLDER"
    source "VENV-FOLDER/bin/activate"
    pip3 install -r requirements.txt
