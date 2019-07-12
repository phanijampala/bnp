from bnp import *

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise RuntimeError("Missing command line input argument: xml file")

        input_file_name = sys.argv[1]
        if not os.path.exists(input_file_name):
            raise RuntimeError("Input file: " + input_file_name + " does not exist")

        tb = CorrelationTable()
        tb.process_input_file("test.xml")
        tb.write_output()

    except Exception as inst:
        print('Exception: ' + str(inst))
