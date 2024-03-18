# chainreport-converter
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.md)
[![de](https://img.shields.io/badge/lang-de-green.svg)](https://github.com/nacrul-eth/chainreport-converter/blob/main/README.de.md)

Converter tools for <https://chain.report/> in collaboration with <https://kryptowoelfe.de/>

## Usage
There is a GUI application available for Windows (.exe).
You can start the GUI application manually on Linux, Mac (and Windows) (with python3, kivy and MyPDF2 installed) as described in the Development section: 

![grafik](https://github.com/nacrul-eth/chainreport-converter/assets/145897591/854117f9-0a94-4e35-8b91-5351e1a0cb1e)


Alternativly you can create a chainreport csv-file by executing the following command line:

    python3 src/chainreport-converter.py "exchange type" "input-file" "output-file"
    => python3 src/chainreport_converter_script.py Hi hi-statement.pdf chainreport.csv

## Current support
Currently the following exchanges/blockchains are supported:

- Hi (<https://hi.com>): CSV Original, but limited version (No withdraw amounts in the Hi statement) or New, PDF based version with all transactions supported
- Plutus (<https://plutus.it>): Csv Rewards export only using the Plutus Dashboard extension as described in the [Wiki](https://github.com/nacrul-eth/chainreport-converter/wiki/PlutusParserCsv)


For additional blockchain/exchange support please open a github-ticket or join the kryptowoelfe telegram (german crypto community) 

[@Krypto_Woelfe](https://t.me/kryptowoelfe)

## Development or Manual run
First set up the development/runtime environment as described [below](#-Initial-setup).

Then start the application via:

    git clone https://github.com/nacrul-eth/chainreport-converter
    cd chainreport-converter/
    install -r requirements.txt
    python3 src/chainreport_converter_app.py

For better maintainability consider the usage of a venv environment is suggested to avoid any unexpected changes:

    python3 -m venv "VENV-FOLDER"
    source "VENV-FOLDER/bin/activate"
    pip3 install -r requirements.txt

## Intial setup
### Linux
Intall git and python3 according to your distributions packages manager, usually "apt install git python3" or "zypper in git python3" ...
### Mac
Install Homebrew fist and the git and python3 via: 

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install git python

### Windows
Download and install git (https://git-scm.com/download/win) and python3 (https://www.python.org/downloads/windows/)

