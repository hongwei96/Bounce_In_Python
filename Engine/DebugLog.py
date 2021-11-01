class Debug:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    @staticmethod
    def Log(msg):
        print(f"{Debug.OKBLUE}Info: {msg}{Debug.ENDC}")
    @staticmethod
    def Warn(msg):
        print(f"{Debug.WARNING}Warning: {msg}{Debug.ENDC}")
    @staticmethod
    def Error(msg):
        print(f"{Debug.FAIL}Error: {msg}{Debug.ENDC}")