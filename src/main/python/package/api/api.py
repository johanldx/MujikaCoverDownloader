import deezer, urllib.request, os

class Deezer():
    def __init__(self, album_name:str):
        self.client = deezer.Client()
        self.album_name = album_name

    def find_album(self):
        """Trouver les albums correspondant dans la base de donnée de Deezer

        Returns:
            dict: Albums
        """
        result = dict()
        request = self.client.search_albums(self.album_name)
        if len(request) > 0:
            for i in range(len(request)):
                album = request[i]
                result[album.id] = {"title": album.title, "artist": album.artist.name, "cover": album.cover_xl}
            return result
        else:
            return None


class FormatFileName():
    def __init__(self, title:str, artist:str):
        self.title = title
        self.artist = artist

    def format_file_name(self):
        """Formatage d'un nom d'album et son artiste en nom de fichier

        Returns:
            str: Nom de fichier formaté
        """
        return ''.join(filter(str.isalnum, self.title)) + "_" + ''.join(filter(str.isalnum, self.artist)) + ".jpg"


class Download():
    def __init__(self, url:str, name:str):
        self.url = url
        self.name = name

    def download(self):
        """Téléchargement d'une pochette d'album

        Returns:
            bool: Téléchargement
        """
        try:
            folder = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop\\albums\\"
            if not os.path.exists(folder):
                os.mkdir(folder)
            f = open(os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop\\albums\\" + self.name,'wb')
            f.write(urllib.request.urlopen(self.url).read())
            f.close()
            return True
        except:
            return False