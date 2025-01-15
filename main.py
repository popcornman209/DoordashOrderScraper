import sys,os, json

args = sys.argv

templateLoginJson = {
    "autoLogin": True,
    "DDusername": "",
    "DDpassword": ""
}
if not os.path.exists("configs/loginInfo.json"):
    with open("configs/loginInfo.json","w") as f: #loads xpaths and classes
        json.dump(templateLoginJson,f)
if not os.path.exists("data/"):
    os.mkdir("data")

print("\033c\033[3J\033[95m--DoorDash order bot--\nby Leo :)\033[0m")

if "--help" in args:
    print("--days: sets amount of days to check in the past, if not provided you will be asked\n--headless: runs in headless mode, fully in tty\n--force-display-browser: forces the browser to open\n--output x: saves results to a file, formatted as json\n--help: this page :)")
else:
    days = -1
    if "--days" in args:
        days = int(args[args.index("--days")+1])
        print("loading {} days".format(days))

    if "--headless" in args:
        outputFile = None
        if "--output" in args:
            outputFile = args[args.index("--output")+1]
            print("saving output to {}".format(outputFile))
        print("running in headless mode!")
        import lib.mainScript as mScript
        mScript.main(True,"--force-display-browser" not in args,days,savePath=outputFile)
    else:
        import lib.gui
        lib.gui.run()