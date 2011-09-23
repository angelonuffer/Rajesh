import time
import unittest
import doctest
import os
import sys
from multiprocessing import Process
from splinter.browser import Browser
import rajesh

def start_rajesh(applications):
    global rajesh_process
    rajesh_process = Process(target=rajesh.run, args=(8080, applications))
    rajesh_process.start()
    time.sleep(1)

def stop_rajesh():
    rajesh_process.terminate()

def load_tests(loader, tests, ignore):
    global browser
    browser = Browser("chrome")
    browser.wait_time = 1
    for test_path in filter(lambda path: path.endswith(".rst"), os.listdir("docs")):
        tests.addTests(doctest.DocFileSuite(os.path.join("docs", test_path),
                                            globs={
                                                "rajesh": rajesh,
                                                "browser": browser,
                                                "start_rajesh": start_rajesh,
                                                "stop_rajesh": stop_rajesh,
                                            },
                                           )
                      )
    return tests

def finish(exit_code):
    browser.quit()

if __name__ == "__main__":
    sys.exit = finish
    unittest.main()
