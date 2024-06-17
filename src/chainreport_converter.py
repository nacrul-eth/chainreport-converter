"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
from PyPDF2 import PdfReader

from chainreport_parser.hi_parser_csv import HiParserCsv
from chainreport_parser.hi_parser_pdf import HiParserPdf
from chainreport_parser.plutus_parser_csv import PlutusParserCsv
from chainreport_parser.nexo_parser_csv import NexoParserCsv
from chainreport_parser.kraken_parser import KrakenParserCsv
from chainreport_parser.coinbase import CoinbaseParserCsv

class ChainreportConverter():
    """Main Class handling the csv files (open, close) and the conversion of the content"""
    def __init__(self, parsertype, inputfile, outputfile):
        super().__init__()
        self.statistics = {
            "input_linecount": 0,
            "output_linecount": 0, 
            "warnings": 0,
            "errors": 0,
            "ignored": 0
        }
        self.chainreport_filename = outputfile
        self.input_filename = inputfile
        self.parser_type = parsertype
        if self.input_filename.lower().endswith(".pdf"):
            self.inputtype = "pdf"
        elif self.input_filename.lower().endswith(".csv"):
            self.inputtype = "csv"
        else:
            self.inputtype = None
            return

        if parsertype == "Hi":
            if self.inputtype == "csv":
                self.parser = HiParserCsv
            elif self.inputtype == "pdf":
                self.parser = HiParserPdf
        elif parsertype == "Plutus":
            self.parser = PlutusParserCsv
            self.inputtype = "csv"
        elif parsertype == "Nexo":
            self.parser = NexoParserCsv
            self.inputtype = "csv"
        elif parsertype == "Kraken":
            self.parser = KrakenParserCsv
        elif parsertype == "Coinbase":
            self.parser = CoinbaseParserCsv
            self.inputtype = "csv"
        else:
            return

    DATESTRING_CR = 'Zeitpunkt'
    TRANSACTIONTYP_CR = 'Transaktions Typ'
    RECEIVED_AMOUNT_CR = 'Anzahl Eingang'
    RECEIVED_CURRENCY_CR = 'Währung Eingang'
    SENT_AMOUNT_CR = 'Anzahl Ausgang'
    SENT_CURRENCY_CR = 'Währung Ausgang'
    TRANS_FEE_AMOUNT_CR = 'Transaktionsgebühr'
    TRANS_FEE_CURRENCY_CR = 'Währung Transaktionsgebühr'
    ORDERID_CR = 'Oder-ID der Exchange'
    DESCRIPTION_CR = 'Beschreibung'

    def write_row(self, csv_writer, input_line, _logging_callback):
        """Write the row into the csv file"""
        csv_writer.writerow({self.DATESTRING_CR: input_line.get_date_string(),
                             self.TRANSACTIONTYP_CR: input_line.get_transaction_type(),
                             self.RECEIVED_AMOUNT_CR: input_line.get_received_amount(),
                             self.RECEIVED_CURRENCY_CR: input_line.get_received_currency(),
                             self.SENT_AMOUNT_CR: input_line.get_sent_amount(),
                             self.SENT_CURRENCY_CR: input_line.get_sent_currency(),
                             self.TRANS_FEE_AMOUNT_CR: input_line.get_transaction_fee_amount(),
                             self.TRANS_FEE_CURRENCY_CR: input_line.get_transaction_fee_currency(),
                             self.ORDERID_CR: input_line.get_order_id(),
                             self.DESCRIPTION_CR: input_line.get_description()})
        self.statistics["output_linecount"] += 1
        if input_line.get_transaction_type() == 'ERROR':
            self.log_error(input_line.get_input_string(), _logging_callback)

    def log_error(self, linedata, _logging_callback):
        """Log the error via callback and update statistics"""
        self.statistics["errors"] += 1
        if _logging_callback:
            _logging_callback("Please report line " + str(self.statistics["output_linecount"]) +
                            "\n" + str(linedata) + "\nThis has to be fixed.")

    def convert_pdf(self, csv_writer, _logging_callback = None):
        """Convert the input pdf to a compatible chainreport file depending on the parser selection"""

        reader = PdfReader(self.input_filename)
        saved_linedata = None
        saved_withdrawdata = None

        for page in reader.pages:
            text = page.extract_text().split("\n")
            for line in text:
                # Use the 20th century for selection, dont expect hi to be around after 2100 ;)
                if line.startswith("20"):
                    self.statistics["input_linecount"] += 1
                    current_linedata = self.parser(line)

                    if current_linedata.check_if_skip_line():
                        self.statistics["ignored"] += 1
                        continue

                    # Combine the multiline trade transaction (if there is still a next line left)
                    if (current_linedata.get_description() in self.parser.TRADETRANSACTION
                            and self.parser == HiParserPdf):
                        # Store current (first) line of the multiline transaction
                        if not saved_linedata:
                            saved_linedata = current_linedata
                            continue
                        # Or handle both lines and reset the saved_linedata
                        self.handle_trade_transactions(csv_writer, saved_linedata, current_linedata)
                        saved_linedata = None
                        continue

                    # Handle withdrawactions (store them first in case they get canceled later)
                    if current_linedata.get_description() in self.parser.WITHDRAWTRANSACTION:
                        if saved_withdrawdata:
                            self.write_row(csv_writer, saved_withdrawdata, _logging_callback)
                        saved_withdrawdata = current_linedata
                        continue

                    # Check cancel of the transaction first
                    if current_linedata.get_description() in self.parser.CANCELTRANSACTION:
                        saved_withdrawdata = None
                        continue

                    # If you ended up here, write data into the file
                    self.write_row(csv_writer, current_linedata, _logging_callback)

        # Write all stored lines at the end as well
        if saved_withdrawdata:
            self.write_row(csv_writer, saved_withdrawdata, _logging_callback)
        if saved_linedata:
            if _logging_callback:
                _logging_callback("Please fix the line " + str(self.statistics["output_linecount"]) +
                                        ". A multi-line transaction only had 1 line")
            self.statistics["errors"] += 1

    def convert_csv(self, csv_writer, _logging_callback):
        """Convert the input csv to a compatible chainreport file depending on the parser selection"""

        with open(self.input_filename, newline='', encoding="utf-8") as csvinput:
            try:
                for line in range(self.parser.SKIPINITIALLINES):
                    csvinput.readline()
            except AttributeError:
                # Expected behaviour for csv files without useless content in the first lines
                _logging_callback("")

            reader = csv.DictReader(csvinput, delimiter=self.parser.DELIMITER)

            saved_linedata = None
            saved_withdrawdata = None

            for line in reader:
                self.statistics["input_linecount"] += 1
                current_linedata = self.parser(line)
                if current_linedata.check_if_skip_line():
                    self.statistics["ignored"] += 1
                    continue

                # Combine the multiline trade transaction (if there is still a next line left)
                if (current_linedata.get_description() in self.parser.TRADETRANSACTION
                        and (self.parser in [HiParserCsv, KrakenParserCsv])):
                    # Store current (first) line of the multiline transaction
                    if not saved_linedata:
                        saved_linedata = current_linedata
                        continue
                    # Or handle both lines and reset the saved_linedata
                    self.handle_trade_transactions(csv_writer, saved_linedata, current_linedata)
                    saved_linedata = None
                    continue

                # Handle withdrawactions (store them first in case they get canceled later)
                if current_linedata.get_description() in self.parser.WITHDRAWTRANSACTION:
                    if saved_withdrawdata:
                        self.write_row(csv_writer, saved_withdrawdata, _logging_callback)
                        self.log_warning(_logging_callback)
                    saved_withdrawdata = current_linedata
                    continue

                # Check cancel of the transaction first
                if current_linedata.get_description() in self.parser.CANCELTRANSACTION:
                    saved_withdrawdata = None
                    continue

                # If you ended up here, write data into the file
                self.write_row(csv_writer, current_linedata, _logging_callback)

        # Write all stored lines at the end as well
        if saved_withdrawdata:
            self.write_row(csv_writer, saved_withdrawdata, _logging_callback)
            self.log_warning(_logging_callback)
        if saved_linedata:
            self.log_error(saved_linedata, _logging_callback)

        csvinput.close()

    def log_warning(self, _logging_callback):
        """
        Log a warning message if the amount is 0 in the export file.

        Parameters:
        _logging_callback (function): A callback function to handle logging. If None, no logging is performed.

        Returns:
        None

        Raises:
        None

        The function checks if the parser is HiParserCsv and if a logging callback function is provided.
        If both conditions are met, it logs a warning message indicating the line number where the amount is 0.
        It also increments the warning count in the statistics dictionary.
        """
        if self.parser == HiParserCsv:
            if _logging_callback:
                _logging_callback("Please fix the line " + str(self.statistics["output_linecount"]) +
                                    ". The amount is 0 in the export file.")
            self.statistics["warnings"] += 1


    def convert(self, _logging_callback = None):
        """Main conversion function: 
        Convert the input file to a compatible chainreport file depending on the parser selection"""

        with open (self.chainreport_filename, 'w', newline='', encoding="utf-8") as csvoutput:
            fieldnames = [self.DATESTRING_CR, self.TRANSACTIONTYP_CR,
                        self.RECEIVED_AMOUNT_CR, self.RECEIVED_CURRENCY_CR,
                        self.SENT_AMOUNT_CR, self.SENT_CURRENCY_CR,
                        self.TRANS_FEE_AMOUNT_CR, self.TRANS_FEE_CURRENCY_CR,
                        self.ORDERID_CR, self.DESCRIPTION_CR ]
            writer = csv.DictWriter(csvoutput, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()

            if self.inputtype == "pdf":
                self.convert_pdf(writer, _logging_callback)
            elif self.inputtype == "csv":
                self.convert_csv(writer, _logging_callback)
            csvoutput.close()

        if _logging_callback:
            _logging_callback("""
            ----------------------------------------------------------------------
            Read lines: """ + str(self.statistics["input_linecount"]) + """
            Written lines: """ + str(self.statistics["output_linecount"]))
            if self.statistics["warnings"] != 0:
                _logging_callback("""
            Number of Warnings: """ + str(self.statistics["warnings"]) + """ - Please check above""")
            if self.statistics["errors"] != 0:
                _logging_callback("""
            Number of Errors: """ + str(self.statistics["errors"]) + """ - Please report them""")
            _logging_callback("""
            For more details check here:
            https://github.com/nacrul-eth/chainreport-converter/wiki/HiParser/""" + self.parser.NAME + """
            ----------------------------------------------------------------------""")

    def handle_trade_transactions(self, writer, current_linedata, next_linedata):
        """Special handling for 2 line trade transactions with Hi"""
        receive_amount = ""
        receive_currency = ""
        sent_amount = ""
        sent_currency = ""
        transaction_fee = ""
        transaction_currency = ""

        if current_linedata.get_received_amount():
            receive_amount = current_linedata.get_received_amount()
            receive_currency = current_linedata.get_received_currency()
            sent_amount = next_linedata.get_sent_amount()
            sent_currency = next_linedata.get_sent_currency()
        else:
            receive_amount = next_linedata.get_received_amount()
            receive_currency = next_linedata.get_received_currency()
            sent_amount = current_linedata.get_sent_amount()
            sent_currency = current_linedata.get_sent_currency()

        if current_linedata.get_transaction_fee_amount() != "0":
            transaction_fee = current_linedata.get_transaction_fee_amount()
            transaction_currency = current_linedata.get_transaction_fee_currency()
        else:
            transaction_fee = next_linedata.get_transaction_fee_amount()
            transaction_currency = next_linedata.get_transaction_fee_currency()

        writer.writerow({self.DATESTRING_CR: current_linedata.get_date_string(),
                                         self.TRANSACTIONTYP_CR: current_linedata.get_transaction_type(),
                                         self.RECEIVED_AMOUNT_CR: receive_amount,
                                         self.RECEIVED_CURRENCY_CR: receive_currency,
                                         self.SENT_AMOUNT_CR: sent_amount,
                                         self.SENT_CURRENCY_CR: sent_currency,
                                         self.TRANS_FEE_AMOUNT_CR: transaction_fee,
                                         self.TRANS_FEE_CURRENCY_CR: transaction_currency,
                                         self.ORDERID_CR: current_linedata.get_order_id(),
                                         self.DESCRIPTION_CR: current_linedata.get_description()})
        self.statistics["output_linecount"] += 1
