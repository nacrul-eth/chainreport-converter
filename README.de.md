# chainreport-converter
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.md)
[![de](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.de.md)


Konverter Tool für <https://chain.report/> in Zusammenarbeit mit <https://kryptowoelfe.de/>

Es gibt als offizielle Release eine Windows Applikation (.exe / https://github.com/nacrul-eth/chainreport-converter/releases), welche auch unter Linux läuft (vorausgesetzt python3, kivy und MyPDF2 sind installiert). 

![grafik](https://github.com/nacrul-eth/chainreport-converter/assets/145897591/854117f9-0a94-4e35-8b91-5351e1a0cb1e)

 
Alternativ kann eine chainreport CSV-Datei erzeugt werden mit dem folgenden Befehl:

    python3 src/chainreport-converter.py "exchange type" "input-file" "output-file"
    => python3 src/chainreport_converter_script.py Hi-PDF hi-statement.csv chainreport.csv


Aktuell werden die folgenden Exchanges/Blockchains unterstützt:

- Hi-CSV (<https://hi.com>): Original, but limited version (No withdraw amounts in the Hi statement)
- Hi-PDF (<https://hi.com>): New, PDF based version with all transactions supported
- Plutus (<https://plutus.it>) (Rewards export only)

Für weitere Blockchain/Exchange Anbindungen bitte ein github-Ticket öffnen oder im Kryptwölfe Telegram nachfragen:

[@Krypto_Woelfe](https://t.me/kryptowoelfe)
