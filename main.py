import sys,os, json

args = sys.argv

templateLoginJson = {
    "autoLogin": True,
    "DDusername": "",
    "DDpassword": ""
}
if "loginInfo.json" not in os.listdir("configs/"):
    with open("configs/loginInfo.json","w") as f: #loads xpaths and classes
        json.dump(templateLoginJson,f)

print("\033c\033[3J\033[95m--DoorDash order bot--\nby Leo :)\033[0m")

if "--help" in args:
    print("--days: sets amount of days to check in the past, if not provided you will be asked\n--headless: runs in headless mode, fully in tty\n--force-display-browser: forces the browser to open\n--help: this page :)")
else:
    days = -1
    if "--days" in args:
        days = int(args[args.index("--days")+1])
        print("loading {} days".format(days))

    if "--headless" in args:
        print("running in headless mode!")
        import lib.mainScript as mScript
        mScript.main(True,"--force-display-browser" not in args,days)
    else:
        import lib.gui
        lib.gui.run()