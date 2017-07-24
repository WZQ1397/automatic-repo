#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import shutil
import os
import subprocess
import codecs
import locale
import sys

mswindows = (sys.platform == "win32")  # learning from 'subprocess' module
if not mswindows:
    print "Only Microsoft Windows Be Supported"
    sys.exit(1)


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

# 'files_to_remove' can be a filename path(type: str) or a set of filenames(type: list)
files_to_remove = "" or [
    'C:\Users\Guodong\AppData\Roaming\Tencent\QQ\Misc\com.tencent.advertisement',
    'C:\Users\Guodong\Documents\WeChat Files\chris-dj\Image\Image',
    'C:\Users\Guodong\Documents\WeChat Files\chris-dj\Image\HttpImage',
    'C:\Users\Guodong\Documents\WeChat Files\chris-dj\Attachment',
]


def confirm(question, default=True):
    """
    Ask user a yes/no question and return their response as True or False.

    :parameter question:
    ``question`` should be a simple, grammatically complete question such as
    "Do you wish to continue?", and will have a string similar to " [Y/n] "
    appended automatically. This function will *not* append a question mark for
    you.
    The prompt string, if given,is printed without a trailing newline before reading.

    :parameter default:
    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``default=False``.

    :return True or False
    """
    # Set up suffix
    if default:
        # suffix = "Y/n, default=True"
        suffix = "Y/n"
    else:
        # suffix = "y/N, default=False"
        suffix = "y/N"
    # Loop till we get something we like
    while True:
        response = raw_input("%s [%s] " % (question, suffix)).lower()
        # Default
        if not response:
            return default
        # Yes
        if response in ['y', 'yes']:
            return True
        # No
        if response in ['n', 'no']:
            return False
        # Didn't get empty, yes or no, so complain and loop
        print("I didn't understand you. Please specify '(y)es' or '(n)o'.")


# TODO(Guodong Ding) save directory itself
def remove_file(path, save_dirs=True):
    path = unicode(path, 'utf8')  # Chinese Non-ASCII character

    def unicode_path(raw_path):
        if isinstance(raw_path, unicode):
            return raw_path
        else:
            return unicode(raw_path, 'utf8')

    def grant_privilege():
        cmd = 'ICACLS ' + path + ' /grant Everyone:F'

        if os.path.isdir(path):
            proc_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
            result = proc_obj.stdout.read().lower().decode(DEFAULT_LOCALE_ENCODING)
            print result

    if os.path.exists(path):
        for top, dirs, nondirs in os.walk(path, followlinks=True):
            # Do delete files
            for item in nondirs:
                try:
                    if os.path.exists(os.path.join(top, item)):
                        os.remove(os.path.join(top, item))
                except WindowsError as e:
                    if e.message:
                        print e.message.decode(DEFAULT_LOCALE_ENCODING)
                    if e.args:
                        print e.args
                    if confirm("Try grant permission/privilege using 'ICACLS'? "):
                        grant_privilege()
                        remove_file(path)

            # Do deal with sub-dirs
            if not save_dirs:
                for item in dirs:
                    try:
                        if os.path.exists(os.path.join(top, item)):
                            shutil.rmtree(os.path.join(top, item))
                    except WindowsError as e:
                        if e.message:
                            print e.message.decode(DEFAULT_LOCALE_ENCODING)
                        if e.args:
                            print e.args
                        if confirm("Try grant permission/privilege using 'ICACLS'? "):
                            grant_privilege()
                            remove_file(path, save_dirs=False)
                            # Skip top dirs


if __name__ == '__main__':
    if not files_to_remove:
        raise RuntimeError('filename not defined or bad cmd parameters.')
    if isinstance(files_to_remove, list):
        for filename in files_to_remove:
            remove_file(filename, save_dirs=True)
    else:
        remove_file(files_to_remove, save_dirs=False)
