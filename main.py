import sys,os, json

args = sys.argv

templateLoginJson = { #tenplate for login info file
    "autoLogin": True,
    "DDusername": "",
    "DDpassword": ""
}
if not os.path.exists("configs/loginInfo.json"): #check if login info file exists, this file isnt on the git for obvious reasons.
    with open("configs/loginInfo.json","w") as f: #open login info file
        json.dump(templateLoginJson,f) #creates template loginInfo file
if not os.path.exists("data/"): #create data folder if it doesnt exist, git doesnt like empty folders :/
    os.mkdir("data")

print("\033[95m--DoorDash order bot--\nby Leo :)\033[0m")

if "--help" in args:
    print("--days: sets amount of days to check in the past, if not provided you will be asked\n--headless: runs in headless mode, fully in tty\n--force-display-browser: forces the browser to open\n--output x: saves results to a file, formatted as json by default\n--output-type x: set to 'json' or 'csv' to say output type\n--help: this page :)")
else:
    days = -1
    if "--days" in args: #get if days flag is used
        days = int(args[args.index("--days")+1]) #get number of days
        print("loading {} days".format(days)) #log to console

    if "--headless" in args: #if running in headless mode
        outputFile = None #set default vals for args
        fileType = "json" # ^^
        if "--output" in args: #if outputted to file
            outputFile = args[args.index("--output")+1] #save file path
            print("saving output to {}".format(outputFile)) #log to console
            if "--output-type" in args: #if custom file type
                fileType = args[args.index("--output-type")+1] #get file type
                print("saving output as {}".format(fileType)) #log
        print("running in headless mode!")
        import lib.mainScript as mScript #import main script
        mScript.main(True,"--force-display-browser" not in args,days,savePath=outputFile,fileType=fileType) #run main script
    else: #running in gui mode
        import lib.gui
        lib.gui.run()