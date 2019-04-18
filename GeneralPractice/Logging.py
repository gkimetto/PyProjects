import logging

extData = {
        'user' : 'gkimetto@redhat.com'
}
def another_function():
    logging.debug("This is a debug-level message",extra =extData)

def main():
    
    #Use basicConfig to configure loging
    # You can customise log with %filename, %funcName, %filename
    fmtstr ="User:%(user)s: %(asctime)s: %(levelname)s: %(funcName)s: Line:%(lineno)d: %(message)s"
    datestr = "%m/%d/%Y %I:%M:%S %p"
    logging.basicConfig(level=logging.DEBUG,
                        filename="output.log",
                        filemode="w",
                        format =fmtstr,
                        datefmt= datestr)
    
    logging.debug("This is a debug message", extra =extData)
    logging.info("This is a Information mesage", extra =extData)
    logging.warning("This is a Warning message", extra =extData)
    logging.error("This is an Error Message", extra =extData)
    logging.critical("THis is a critical message- DO NOT IGNORE", extra =extData)
    str= "string"
    intv=10
    logging.info("Here is a {} variable and an {}".format(str, intv), extra =extData)
    another_function
if __name__ =="__main__":
    main()