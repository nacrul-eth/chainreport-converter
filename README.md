# chainreport-converter
Converter tools for <https://chain.report/> in collaboration with <https://kryptowoelfe.de/>

There is a GUI application available for Windows (.exe), which also can be started on Linux (with python3 and kivy installed): 

![grafik](https://github.com/nacrul-eth/chainreport-converter/assets/145897591/854117f9-0a94-4e35-8b91-5351e1a0cb1e)


Alternativly you can create a chainreport csv-file by executing the following command line / 
Alternativ kann eine chainreport CSV-Datei erzeugt werden mit dem folgenden Befehl:

    python3 src/chainreport-converter.py "exchange type" "input-file" "output-file"
    => python3 src/chainreport_converter_script.py Hi hi-statement.csv chainreport.csv


Currently the following exchanges/blockchains are supported / 
Aktuell werden die folgenden Exchanges/Blockchains unterstützt:

- Hi (<https://hi.com>)
- Plutus (<https://plutus.it>) (Rewards export only)

For additional blockchain/exchange support please open a github-ticket or join the kryptowoelfe telegram / 
Für weitere Blockchain/Exchange Anbindungen bitte ein github-Ticket öffnen oder im Kryptwölfe Telegram nachfragen:

[@Krypto_Woelfe](https://t.me/kryptowoelfe)
