import subprocess
import sys
import argparse
import os
import json
import logging as log

class Base:

    def __init__(self):
        log.basicConfig(filename='mksh.log', filemode='w', level=log.DEBUG)
        #self.setup()
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

    # This function will execute the testcase
    def testcase_execute(self,testcase_name):

        log.info("collecting data from json file ")
        testCaseData = self.readJsonFile(self.jsonFilePath)
        log.info(testcase_name + " '" + testCaseData[str(testcase_name)]["testname"] +"' execution started")

        for key,script in testCaseData[str(testcase_name)]["script"].items():
            self.writeToFile(key, script)
        # execute command
        if isinstance(testCaseData[str(testcase_name)]["cmd"],str):
            log.info("Executing the command '" + testCaseData[str(testcase_name)]["cmd"] + "' for " + testcase_name)
            lang = subprocess.getoutput(testCaseData[str(testcase_name)]["cmd"])
        elif isinstance(testCaseData[str(testcase_name)]["cmd"],list):
            for i in testCaseData[str(testcase_name)]["cmd"]:
                log.info("Executing the command '" + i + "' for " + testcase_name)
                lang = subprocess.getoutput(i)
        else:
            log.info("Invalid command parameter passed")

        expected_op_decode = self.getUTFString(testCaseData[str(testcase_name)]["output"])
        log.info("Expected output for '"+ testcase_name + "' is '" + expected_op_decode +"'")

        if lang != expected_op_decode:
            print(testcase_name+ " : "+testCaseData[str(testcase_name)]["testname"]+ " failed")
            log.info(testcase_name+" failed due to mismatch in actual o/p: \n'" + lang + "' and expected o/p: \n'"+ expected_op_decode +"'")
        else:
            print(testcase_name+ " : "+testCaseData[str(testcase_name)]["testname"]+ " passed")
            log.info(testcase_name+" passed succeffully")


    def All(self):
        print("Running all script")
        log.info("running all scripts/testcases")
        self.testcase_execute("testcase1")
        self.testcase_execute("testcase2")
        self.testcase_execute("testcase3")
        self.testcase_execute("testcase4")
        self.testcase_execute("testcase5")
        self.testcase_execute("testcase6")
        self.testcase_execute("testcase7")


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


