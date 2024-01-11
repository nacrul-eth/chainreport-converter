"""Main Module to parse csv files and create a chainreport compatible version."""

import csv
from PyPDF2 import PdfReader

from chainreport_parser.hi_parser_csv import HiParserCsv
from chainreport_parser.hi_parser_pdf import HiParserPdf
from chainreport_parser.plutus_parser_csv import PlutusParserCsv
from chainreport_parser.nexo_parser_csv import NexoParserCsv

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
        if parsertype == "Hi-CSV":
            self.parser = HiParserCsv
            self.inputtype = "csv"
        elif parsertype == "Hi-PDF":
            self.parser = HiParserPdf
            self.inputtype = "pdf"
        elif parsertype == "Plutus-CSV":
            self.parser = PlutusParserCsv
            self.inputtype = "csv"
        elif parsertype == "Nexo-CSV":
            self.parser = NexoParserCsv
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
        skip_next_line = False
        next_line = ""

        pdf_reader = PdfReader(self.input_filename)
        for page in pdf_reader.pages:
            text = page.extract_text().split("\n")
            for line in text:
                # Use the 20th century for selection, dont expect hi to be around after 2100 ;)
                if line.startswith("20"):
                    self.statistics["input_linecount"] += 1
                    # Populate required parameters only, if they were already initialized
                    if not next_line:
                        next_line = line
                        continue
                    current_line, next_line = next_line, line

                    # Only skip this line, if it contains a valid content (didnt figure out skipping 2 lines yet)
                    if skip_next_line:
                        if line.startswith("20"):
                            skip_next_line = False
                            continue
                        continue

                    current_linedata = self.parser(current_line)
                    next_linedata = self.parser(next_line)

                    # Combine the multiline trade transaction (if there is still a next line left)
                    if (current_linedata.get_description() in self.parser.TRADETRANSACTION
                            and self.parser == HiParserPdf):
                        self.handle_trade_transactions(csv_writer, current_linedata, next_linedata)
                        skip_next_line = True
                        continue
                    # Handle canceled withdrawactions
                    if current_linedata.get_description() in self.parser.WITHDRAWTRANSACTION:
                        # Check for cancel of the transaction first
                        if next_linedata.get_description() in self.parser.CANCELTRANSACTION:
                            # If the Withdraw was canceled, skip both lines
                            skip_next_line = True
                            continue

                    # If you ended up here, write data into the file
                    if current_linedata.get_description() not in (self.parser.EXCLUSIONSTRINGS or
                                                               self.parser.CANCELTRANSACTION):
                        self.write_row(csv_writer, current_linedata, _logging_callback)

    def convert_csv(self, csv_writer, _logging_callback):
        """Convert the plutus csv to a compatible chainreport file depending on the parser selection"""

        with open(self.input_filename, newline='', encoding="utf-8") as csvinput:
            reader = csv.DictReader(csvinput, delimiter=self.parser.DELIMITER)

            for row in reader:
                self.statistics["input_linecount"] += 1
                current_rowdata = self.parser(row)
                if current_rowdata.get_transaction_type() == self.parser.SKIP_STR:
                    continue

                self.write_row(csv_writer, current_rowdata, _logging_callback)
        csvinput.close()
    def convert_hi_csv(self, csv_writer, _logging_callback):
        """Convert the input csv to a compatible chainreport file depending on the parser selection"""

        with open(self.input_filename, newline='', encoding="utf-8") as csvinput:
            reader = csv.DictReader(csvinput, delimiter=self.parser.DELIMITER)
            skip_next_line = False
            next_row = next(reader)

            for row in reader:
                self.statistics["input_linecount"] += 1
                # Populate required parameters
                current_row, next_row = next_row, row

                # Skip this line as well (didnt figure out skipping 2 lines yet)
                if skip_next_line:
                    skip_next_line = False
                    continue
                current_rowdata = self.parser(current_row)
                next_rowdata = self.parser(next_row)
                # maybe sutable for hi-parser as well: whatever needs to be skipped as row type with "Skip"
                if current_rowdata.get_transaction_type() == self.parser.SKIP_STR:
                    continue
                # Combine the multiline trade transaction (if there is still a next line left)
                if current_rowdata.get_description() in self.parser.TRADETRANSACTION and self.parser == HiParserCsv:
                    self.handle_trade_transactions(csv_writer, current_rowdata, next_rowdata)
                    skip_next_line = True
                    continue

                # Handle canceled withdrawactions
                if current_rowdata.get_description() in self.parser.WITHDRAWTRANSACTION:
                    # Check for cancel of the transaction first
                    if next_rowdata.get_description() in self.parser.CANCELTRANSACTION:
                        # If the Withdraw was canceled, skip both lines
                        skip_next_line = True
                        continue
                    if _logging_callback:
                        _logging_callback("Please fix the line " + str(self.statistics["output_linecount"]) +
                                                ". The amount is 0 in the export file.")
                    self.statistics["warnings"] += 1

                # If you ended up here, write data into the file
                if current_rowdata.get_description() not in (self.parser.EXCLUSIONSTRINGS or
                                                                    self.parser.CANCELTRANSACTION):
                    self.write_row(csv_writer, current_rowdata, _logging_callback)
            # Check seperat last line
            if next_rowdata.get_description() not in (self.parser.EXCLUSIONSTRINGS or
                                                                 self.parser.CANCELTRANSACTION):
                self.write_row(csv_writer, next_rowdata, _logging_callback)
        csvinput.close()


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
                if self.parser_type == "HI-CSV":
                    self.convert_hi_csv(writer, _logging_callback)
                else:
                    self.convert_csv(writer, _logging_callback)
            csvoutput.close()

        if _logging_callback:
            _logging_callback("""
            ----------------------------------------------------------------------
            Read lines: """ + str(self.statistics["input_linecount"]) + """
            Written lines: """ + str(self.statistics["output_linecount"]) + """
            Number of Warnings: """ + str(self.statistics["warnings"]) + """ - Please check above
            Number of Errors: """ + str(self.statistics["errors"]) + """ - Please report them
            Please check details here: 
            https://github.com/nacrul-eth/chainreport-converter/wiki/HiParser/""" + self.parser.NAME + """
            ----------------------------------------------------------------------""")

    def handle_trade_transactions(self, writer, current_linedata, next_linedata):
        """Special handling for 2 line trade transactions with Hi"""
        receive_amount = ""
        receive_currency = ""
        sent_amount = ""
        sent_currency = ""

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

        writer.writerow({self.DATESTRING_CR: current_linedata.get_date_string(),
                                         self.TRANSACTIONTYP_CR: current_linedata.get_transaction_type(),
                                         self.RECEIVED_AMOUNT_CR: receive_amount,
                                         self.RECEIVED_CURRENCY_CR: receive_currency,
                                         self.SENT_AMOUNT_CR: sent_amount,
                                         self.SENT_CURRENCY_CR: sent_currency,
                                         self.TRANS_FEE_AMOUNT_CR: current_linedata.get_transaction_fee_amount(),
                                         self.TRANS_FEE_CURRENCY_CR: current_linedata.get_transaction_fee_currency(),
                                         self.ORDERID_CR: current_linedata.get_order_id(),
                                         self.DESCRIPTION_CR: current_linedata.get_description()})
        self.statistics["output_linecount"] += 1
