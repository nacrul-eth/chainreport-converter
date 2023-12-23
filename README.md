# chainreport-converter
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.md)
[![de](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.de.md)

Converter tools for <https://chain.report/> in collaboration with <https://kryptowoelfe.de/>

## Usage
There is a GUI application available for Windows (.exe), which also can be started on Linux (with python3, kivy and MyPDF2 installed): 

![grafik](https://github.com/nacrul-eth/chainreport-converter/assets/145897591/854117f9-0a94-4e35-8b91-5351e1a0cb1e)


Alternativly you can create a chainreport csv-file by executing the following command line:

    python3 src/chainreport-converter.py "exchange type" "input-file" "output-file"
    => python3 src/chainreport_converter_script.py Hi hi-statement.csv chainreport.csv

## Current support
Currently the following exchanges/blockchains are supported:

- Hi-CSV (<https://hi.com>): Original, but limited version (No withdraw amounts in the Hi statement)
- Hi-PDF (<https://hi.com>): New, PDF based version with all transactions supported
- Plutus (<https://plutus.it>) (Rewards export only)

For additional blockchain/exchange support please open a github-ticket or join the kryptowoelfe telegram (german crypto community) 

[@Krypto_Woelfe](https://t.me/kryptowoelfe)

## Development
For pull requests and setting up the development environment please use the requirements.txt file. Additionally, the usage of a venv environment is suggested to avoid any unexpected changes:

    python3 -m venv "VENV-FOLDER"
    source "VENV-FOLDER/bin/activate"
    pip3 install -r requirements.txt