import pandas as pd
import tarfile

# Paths to data.tar.gz of the 2 database
path_tarball = './spotify/data/data.tar.gz'

# Name of files who will be created
paths = ["./spotify/data/SpotifyFeatures.csv",
         "./spotify/data/charts.csv"]

def get_data():
    my_tar = tarfile.open(path_tarball)
    my_tar.extractall('./spotify/data')
    my_tar.close()

    df = pd.read_csv(paths[0])
    df2 = pd.read_csv(paths[1])
    
    # Ligne pour couper les dates dont on a pas besoin
    df2 = df.drop(df[df.date != "2021-11-30"].index)

    # Ligne pour réinitialiser l'index
    df2 = df.reset_index(inplace=True)

    # Ligne pour supprimer l'ancienne colonne d'index
    df2 = df.drop(columns=['index', 'level_0'])    
    df2 = df2.drop(columns=['Unnamed: 0'])

    # Ligne pour enelever la typo sur un des genre de musique
    df.loc[df.genre == 'Children’s Music', 'genre'] = 'Children\'s Music'

    # Ligne pour harmoniser les 2 csv
    df = df.rename(columns={'artist_name':'artist', 'track_name':'title'})

    # Ligne pour réecrire la base données
    df.to_csv(paths[0])
    df2.to_csv(paths[1])

    if __name__ == '__main__':
        get_data()