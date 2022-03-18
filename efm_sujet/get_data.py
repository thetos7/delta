import zipfile

def unzip_file(str) :
    zipfile.ZipFile(str, 'r').extractall("data/")

unzip_file("data/artists.zip")
unzip_file("data/album_ratings.zip")
unzip_file("data/tracks.zip")
