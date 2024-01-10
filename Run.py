#!/usr/bin/env python3
import platform, subprocess

if __name__ == '__main__':
    try:
        if platform.machine() == "aarch64":
            subprocess.call(["chmod", "+x", "aarch64"])
            subprocess.call(["./aarch64"])
        elif platform.machine() == "x86_64":
            subprocess.call(["chmod", "+x", "x86_64"])
            subprocess.call(["./x86_64"])
        else:
            print(f"Perangkat {platform.machine()} bit, tidak dapat menjalankan aarch64 atau x86_64!")
            exit()
    except (KeyboardInterrupt):
        subprocess.call(["./x86_64"])
    except (Exception) as e:
        print(f"[Error] {str(e).capitalize()}!")
        exit()