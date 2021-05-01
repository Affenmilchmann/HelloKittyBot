from time import strftime
from os import path as ospath

logs_folder = "logs/"

log_file = ospath.join(ospath.dirname(__file__), logs_folder + "log.txt")
r_log_file = ospath.join(ospath.dirname(__file__), logs_folder + "requests_log.txt")
m_log_file = ospath.join(ospath.dirname(__file__), logs_folder + "msg_log.txt")
err_log_file = ospath.join(ospath.dirname(__file__), logs_folder + "error_log.txt")

def formTimeStamp(format_ = 'd'):
    '''
    formats:
    'h' - H:M:S
    'd' - Y-M-D H:M:S
    '''
    formats = {
        'h': "%H:%M:%S",
        'd': "%Y-%m-%d %H:%M:%S"
    }
    return strftime(formats[format_])

def formLogStamp(type_ = "i", format_ = 'd'):
    '''
    type_ can be
    'i' - Info
    'w' - Warn
    'e' - Error 
    '''
    types = {
        'i': "Info ",
        'w': "Warn ",
        'e': "Error"
    }
    return "[" + types[type_] + " " + formTimeStamp(format_) + "] "

def consoleOutput(message, type_ = "i", format_ = 'd'):
    print(formLogStamp(type_, format_), message)

def logsCheck():
    def fileCheck(file_name):
        try: 
            with open(file_name, 'r') as f:
                pass
        except IOError:
            consoleOutput(file_name + " is missing.", 'w')
            try:
                with open(file_name, 'w') as f:
                    f.write(formLogStamp('i', 'd') + "File created.\n")
                consoleOutput(file_name + " was created.", 'i')
            except IOError:
                consoleOutput('failed to create ' + file_name, 'e')


    fileCheck(log_file)
    fileCheck(r_log_file)
    fileCheck(m_log_file)
    fileCheck(err_log_file)

    consoleOutput("Logs are checked.", 'i')


def log(message, file_name, type_ = 'i'):
    with open(file_name, 'a') as f:
        f.write(formLogStamp(type_) + str(message) + "\n")

def msgLog(message, from_, to_):
    log("From: " + str(from_) + " To: " + str(to_) + ". '" + str(message) + "'", m_log_file)

def reqLog(req):
    log(req, r_log_file)

def errLog(err):
    log(err, err_log_file)

def botLog(msg):
    log(str(msg), log_file)