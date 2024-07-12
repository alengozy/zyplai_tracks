from src.artists.schemas import ArtistImportModel
from src.tracks.schemas import TrackImportModel
from pydantic import ValidationError


def convert_to_model_objects(df):
    model_objects = []
    artists = {}  # Dictionary to store created Artist objects

    for index, row in df.iterrows():
        artist_id = row['artist_id']
        if artist_id not in artists:
            try:
                artist = ArtistImportModel(**row[['id', 'name']])  # Extract artist data
                artists[artist_id] = artist
            except ValidationError as e:
                print(f"Error creating Artist for row {index+1}: {e}")
                continue  # Skip to next row if artist creation fails

        try:
            album_id = row.get('album_id')  # Handle potential missing album data
            track = TrackImportModel(
                title=row['title'],
                artist_id=artist_id,
                album_id=album_id,
            )
            model_objects.append(track)
        except ValidationError as e:
            print(f"Error creating Track for row {index+1}: {e}")

    return model_objects