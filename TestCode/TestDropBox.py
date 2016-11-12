import datetime
import dropbox
import os
import time

# Have created a Dropbox App folder with the DropBox Developer console
# https://www.dropbox.com/developers/apps

# Get the access token from a file, as created by above console
def get_dropboxkey():
    with open('DropBoxKey.conf', 'r') as f:
        key = f.readline()
    f.close()
    return key


# Simplified upload from the updown.py example
# https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py
def upload(sourcefile, destfile, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(sourcefile)
    with open(sourcefile, 'rb') as f:
        data = f.read()
    try:
        res = dbx.files_upload(
            data, destfile, mode,
            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
            mute=True)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None
    print 'Uploaded', res.name.encode('utf8')
    return res


def purge_old_files(daystokeep):
    files = 0
    print 'Deleting dropbox files older than {} days'.format(daystokeep)
    now = datetime.datetime.now()
    for entry in dbx.files_list_folder('').entries:
        delta = now - entry.server_modified
        if delta.days > daystokeep:
            files += 1
            print 'Deleting {} from {}'.format(entry.name,entry.server_modified)
            try:
                dbx.files_delete('/'+entry.name)
            except dropbox.exceptions.ApiError as err:
                print('*** API error', err)
                return None
    if files > 0:
        print 'Deleted {} files'.format(files)

#Test code
dbx = dropbox.Dropbox(get_dropboxkey())
purge_old_files (30)
upload('CaptureOutput2016-05-19T205313.679536.jpg', '/CaptureOutput2016-05-19T205313.679536.jpg', True)
