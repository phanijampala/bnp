import unittest
from bnp import *

class TradeBoardUniTest(unittest.TestCase):
    def test_BNP_input(self):
        tb = CorrelationTable()
        tb.add_entry("234", 3, 1000, 100, 654)
        tb.add_entry("234", 3, 1000, 200, 135)
        tb.add_entry("222", 1, 500, 600, 423)
        tb.add_entry("234", 3, 1000, 200, 652)
        tb.add_entry("200", 2, 2000, 1000, 645)
        result = tb.get_output()

        expected_output = [("200", 2, "Pending"), ("222", 1, "Rejected"), ("234", 3, "Accepted")]
        self.assertEqual( result, expected_output)

    def test_xml_input(self):
        input_processor = xml_input_processor()
        input_file_name = "test1.xml"
        with open(input_file_name, "w") as f:
            f.write(
                '''<CorrelationTable>
                        <CorrelationEntry>
                            <CorrelationID>234</CorrelationID>
                            <NumberOfTrades>3</NumberOfTrades>
                            <Limit>1000</Limit>
                            <Value>100</Value>
                            <TradeId>654</TradeId>
                        </CorrelationEntry>
                       <CorrelationEntry>
                            <CorrelationID>222</CorrelationID>
                            <NumberOfTrades>1</NumberOfTrades>
                            <Limit>500</Limit>
                            <Value>600</Value>
                            <TradeId>423</TradeId>
                        </CorrelationEntry>
                    </CorrelationTable>'''
            )

        entry1 = xml_input_processor.xml_entry()
        entry1.correlation_id = '234'
        entry1.number_of_trades = 3
        entry1.limit = 1000
        entry1.value = 100
        entry1.trade_id = 654

        entry2 = xml_input_processor.xml_entry()
        entry2.correlation_id = '222'
        entry2.number_of_trades = 1
        entry2.limit = 500
        entry2.value = 600
        entry2.trade_id = 423

        found_entries = input_processor.get_trade_entries(input_file_name)

        self.assertEqual(len(found_entries), 2)
        self.assertEqual(str(found_entries[0]), str(entry1))
        self.assertEqual(str(found_entries[1]), str(entry2))
        os.remove(input_file_name)

if __name__ == '__main__':
    unittest.main()