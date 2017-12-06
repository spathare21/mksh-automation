import subprocess
import sys
import argparse
import os
import json
import logging as log

class Base:

    def __init__(self):
        try:
            os.remove("append.txt")
        except OSError:
            pass
        log.basicConfig(filename='mksh.log', filemode='w', level=log.DEBUG)
        self.setup()
        self.jsonFilePath="config.json"


    # Initializing test environment
    def setup(self):
        log.info("Setup SJIS environment")
        os.system("localedef -f SHIFT_JIS -i ja_JP ja_JP.SJIS")
        os.system("LANG=ja_JP.SJIS")

        log.info("ja_JP.SJIS encoding compiled and set")

        lang = subprocess.getoutput("echo $LANG")
        log.info("Check ja_jp language set")
        if lang != "ja_JP.SJIS":
            print("error")
            log.debug("error while setting language Lang=ja_Jp.SJIS")
            sys.exit()
        else:
            log.info("LANGja_JP set successfully")

    # read json data from file
    def readJsonFile(self, filename):
        with open(filename, 'r') as f:
            log.info("reading testcase data from json file '"+ filename +"'")
            data = json.load(f)
        return data

    # Creating .mksh script data to file
    def writeToFile(self, filename, data):
        log.info("Writing data to file '"+ filename +"'")
        script_file = open(filename, "w", encoding='utf-8')
        script_file.write(data)
        log.info("Data writen succeefully in file")
        script_file.close()

    # Convert string into utf-8 string
    def getUTFString(self, character):
        expected_op_encode = character.encode("utf-8")
        log.info("Converted string to utf-8 format '"+ expected_op_encode.decode("utf-8") +"'")
        return expected_op_encode.decode("utf-8")

    # Execute commands
    def execute_command(self, cmd, testcase_name):
        output_list = list()
        if isinstance(cmd, str):
            log.info("Executing the command '" + cmd + "' for " + testcase_name)
            output_list.append(subprocess.getoutput(cmd))
        elif isinstance(cmd,list):
            for i in cmd:
                log.info("Executing the command '" + i + "' for " + testcase_name)
                output_list.append(subprocess.getoutput(i))
        else:
            log.info("Invalid command parameter passed")
            return False

        return output_list

    #Verify actual output and expected output
    def verify_output(self, actual_output, expected_output):
        if isinstance(expected_output, str):
            expected_op_decode = self.getUTFString(expected_output)
            log.info("\nActual output: "+ str(actual_output) + "\nExpected output: "+ str(expected_output))
            if actual_output[-1] != expected_op_decode:
                return False
            else:
                return True
        elif isinstance(expected_output, list):
            for i in range(len(actual_output)):
                expected_op_decode = self.getUTFString(expected_output[i])
                log.info("\nActual output: " + str(actual_output) + "\nExpected output: " + str(expected_output))
                if actual_output[i] != expected_op_decode:
                    return False
                else:
                    return True
        else:
            print("Invalid expected output type")
            return False

    # This function will execute the testcase
    def testcase_execute(self,testcase_name):
        log.info("collecting data from json file ")
        testCaseData = self.readJsonFile(self.jsonFilePath)
        log.info(testcase_name + " '" + testCaseData[str(testcase_name)]["testname"] +"' execution started")

        for key,script in testCaseData[str(testcase_name)]["script"].items():
            self.writeToFile(key, script)

        cmd_output = self.execute_command(testCaseData[str(testcase_name)]["cmd"], testcase_name)
        if self.verify_output(cmd_output, testCaseData[str(testcase_name)]["output"]):
            print(testcase_name + " : " + testCaseData[str(testcase_name)]["testname"] + " - passed succeffully")
            log.info(testcase_name + " : " + testCaseData[str(testcase_name)]["testname"] + " - passed succeffully")
        else:
            print(testcase_name + " : " + testCaseData[str(testcase_name)]["testname"] + " failed")
            log.info(testcase_name + " : " + testCaseData[str(testcase_name)]["testname"] + " failed")


    def All(self):
        print("Running all script")
        log.info("Running all scripts/testcases")
        self.testcase_execute("testcase1")
        self.testcase_execute("testcase2")
        self.testcase_execute("testcase3")
        self.testcase_execute("testcase4")
        self.testcase_execute("testcase5")
        self.testcase_execute("testcase6")
        self.testcase_execute("testcase7")
        self.testcase_execute("testcase8")


if __name__ == "__main__":

    obj = Base()

    parser = argparse.ArgumentParser()
    parser.add_argument('--test',help="test case name",default="All")
    args = parser.parse_args()
    if args.test != "All":
        try:
            getattr(obj,"testcase_execute")(args.test)
        except Exception as e:
            print(str(e)+" testcase doesnot exist")
    else:
        getattr(obj, "All")()


