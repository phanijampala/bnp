
import datetime
import sys
import os
import xml.sax

def append_log_entry(text):
    with open("server.log", "a") as f:
        f.write(str(datetime.datetime.now()) + "|" + text + "\n")

class CorrelationEntry():
    def __init__(self, num_of_trades, limit):
        self.num_of_trades_expected =  num_of_trades
        self.limit = limit
        self.total_trade_value = 0
        self.num_of_trades_encountered = 0
        self.trade_ids = set()

    def append_trade(self, value, trade_id):
        self.total_trade_value += value
        self.num_of_trades_encountered += 1
        self.log_message(value, trade_id)

    def log_message(self, value, trade_id):
        append_log_entry("Found Trade id: " + str(trade_id) + " with value: " + str(value))

        if trade_id in self.trade_ids:
            append_log_entry("Duplicate Trade id: " + str(trade_id) + " with value: " + str(value))
        else:
            self.trade_ids.add(trade_id)

        if self.total_trade_value > self.limit:
            append_log_entry("Trade id : " + str(trade_id) + " with value: " + str(value) + " exceeds limit: " + str(self.limit))

        if self.num_of_trades_encountered > self.num_of_trades_expected:
            append_log_entry("Not expected Trade id: " + str(trade_id) + " with value: " + str(value))


    def get_status(self):
        if self.num_of_trades_encountered < self.num_of_trades_expected:
           return "Pending"

        if self.total_trade_value <= self.limit:
            return "Accepted"
        else:
            return "Rejected"

class CorrelationTable():
    def __init__(self):
        self.correlation_entries = {}

    def add_entry(self, correlation_id, num_of_trades, limit, value, trade_id):
        if correlation_id not in self.correlation_entries:
            self.correlation_entries[correlation_id] = CorrelationEntry(num_of_trades, limit)

        self.correlation_entries[correlation_id].append_trade(value, trade_id)

    def get_output(self):
        result = []
        for key in sorted(self.correlation_entries.keys()):
            value = self.correlation_entries[key]
            result.append( (key,value.num_of_trades_expected, value.get_status()) )
        return result

    def write_output(self):
        output_file_name = "results.csv"
        with open(output_file_name, 'w') as f:
            f.write("CorrelationID, NumberOfTrades, State\n")
            for corr_id, trades_expected, status in self.get_output():
                f.write(corr_id + "," + str(trades_expected)+ "," + status + "\n")


    def process_input_file(self, file_name):
        input_processor = xml_input_processor()
        xml_entries = input_processor.get_trade_entries(file_name)
        for entry in xml_entries:
            self.add_entry(entry.correlation_id, entry.number_of_trades, entry.limit, entry.value, entry.trade_id)

class xml_input_processor():
    class xml_entry():
        def __init__(self):
            self.correlation_id = ""
            self.number_of_trades = 0
            self.limit = 0
            self.value = 0
            self.trade_id = 0

        def __str__(self):
            return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__]) + "\n"

    class xml_input_handler(xml.sax.ContentHandler):
        def __init__(self):
            self.entries = []

        def startElement(self, tag, attributes):
            if tag == "CorrelationEntry":
                self.entry = xml_input_processor.xml_entry()
            self.current_data = tag

        def endElement(self, tag):
            if tag == "CorrelationEntry":  # we have hit the end node
                self.entries.append(self.entry)
                del self.entry

            self.current_data = ""

        def characters(self, content):
            if self.current_data == "CorrelationID":
                self.entry.correlation_id = content
            elif self.current_data == "NumberOfTrades":
                self.entry.number_of_trades = int(content)
            elif self.current_data == "Limit":
                self.entry.limit = int(content)
            elif self.current_data == "Value":
                self.entry.value = int(content)
            elif self.current_data == "TradeId":
                self.entry.trade_id = int(content)

    def get_trade_entries(self, file_name):
        parser = xml.sax.make_parser()
        xml_handler = xml_input_processor.xml_input_handler()
        parser.setContentHandler(xml_handler)
        parser.parse(file_name)
        return xml_handler.entries

