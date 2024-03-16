import multiprocessing
import time
import datetime

from src.cleaners.cleaner import run as run_cleaner
from src.utilities.logger import SmareLogger

logger = SmareLogger()

def printTime():
    print(datetime.datetime.now().strftime("%H:%M:%S:%f")[:-3])


def timer(duration):
    time.sleep(duration)


def stopwatch():
    seconds = 0
    while True:
        print(seconds)
        seconds += 1
        timer(1)


def module(name, done, logs):
    moduleLog = []

    moduleLog.append(f"running {name}")
    print(f"running {name}")

    i = 0
    # run loop while not done
    while not done.value:
        i += 1

    moduleLog.append(f"counted to {i}")
    moduleLog.append(f"cleaning up for {name}")
    print(f"cleaning up for {name}")

    logs[name] = moduleLog


def runModule(duration, target, version):
    done = multiprocessing.Value("b", False)

    mod = multiprocessing.Process(target=target, args=(done, version))
    mod.start()

    # wait for duration, then stop the module
    logger.debug(f"starting timer for {duration} seconds")
    timer(duration)
    done.value = True
    logger.debug(f"timer finished, set process boolean flag to true")

    # wait until the module process returns
    mod.join()
    logger.debug(f"process completed")


if __name__ == "__main__":
    runModule(20, run_cleaner, 1)
