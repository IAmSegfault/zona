import plistlib

def update():
    plist = None
    with open('appbuild/skel.plist', 'rb') as f:
        plist = plistlib.load(f, fmt=plistlib.FMT_XML)

    if plist is not None:
        name = input("Enter the application name [game]: ")
        version = input("Enter the application version [0.0.0]: ")
        main_program = input("Enter the application starting executable name [maingame]: ")
        if name == "":
            name = "game"
        if version == "":
            version = "0.0.0"
        if main_program == "":
            main_program = "MacOS/maingame"
        else:
            main_program = "MacOS/" + main_program

        plist['CFBundleDisplayName'] = name
        plist['CFBundleIdentifier'] = name
        plist['CFBundleName'] = name
        plist['CFBundleShortVersionString'] = version
        plist['CFBundleExecutable'] = main_program
        print(plist)

        with open('appbuild/Info.plist', 'wb') as f:
            plistlib.dump(plist, f)


if __name__ == '__main__':
    update()
