import sys, lib.gui
import lib.mainScript as mScript

args = sys.argv

print("\033c\033[3J\033[95m--DoorDash order bot--\nby Leo :)")

if "--help" in args:
    print("-d: sets amount of days to check in the past, if not provided you will be asked\n--headless: runs in headless mode, fully in tty\n--help: this page :)")
else:
    if "-d" in args:
        days = args[args.index("-d")+1]
        print("loading {} days".format(days))

    if "--headless" in args:
        print("running in headless mode!")
        mScript.main(False,days)
    else:
        lib.gui.run()