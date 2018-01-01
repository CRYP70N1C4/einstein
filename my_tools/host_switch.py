import ctypes, sys, shutil


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        src = sys.argv[1]
        if is_admin():
            shutil.copy(src, 'C:\Windows\System32\drivers\etc\hosts')
        else:
            params = ' '.join([sys.argv[0]] + sys.argv[1:]);
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
