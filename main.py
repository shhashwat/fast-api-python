from fastapi import FastAPI, HTTPException, Path, Query
from schema import GenreURLChoices, BandBase, BandCreate, BandWithID
from typing import Annotated

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Beatles', 'genre': 'Rock'},
    {'id': 2, 'name': 'The Rolling Stones', 'genre': 'Electronic'},
    {'id': 3, 'name': 'The Who', 'genre': 'Rock'},
    {'id': 4, 'name': 'The Doors', 'genre': 'Pop'},
    {'id': 5, 'name': 'The Roots', 'genre': 'Hip-Hop', 'albums': [
        {'title': 'Things fall apart', 'release_date': '1999-02-23'},
        {'title': 'Undun', 'release_date': '2011-12-06'}
    ]}, 
    {'id': 6, 'name': 'Metallica', 'genre': 'Metal'}, 
]

@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None
) -> list[BandWithID]:
    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: Annotated[int, Path(title='Band ID')]) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)
    if band is None:
        #status code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.get('/bands/all/{genre}')
async def bands_genre_available(genre: GenreURLChoices) -> dict:
    matching_bands = [b['name'] for b in BANDS if b['genre'].lower() == genre.value]

    if not matching_bands:
        #status code 404
        raise HTTPException(status_code=404, detail=f"No bands found for {genre}")
    numbered_bands = [f"{i+1}. {name}" for i, name in enumerate(matching_bands)]
    return {"bands": numbered_bands}

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
    # Convert the input genre to lowercase
    genre_lower = genre.lower()
    
    # Validate if the lowercase genre is in the GenreURLChoices enum
    if genre_lower not in [g.value for g in GenreURLChoices]:
        raise HTTPException(status_code=400, detail=f"Invalid genre: {genre}. Valid genres are: {[g.value for g in GenreURLChoices]}")
    
    # Filter bands by the lowercase genre
    return [
        b for b in BANDS if b['genre'].lower() == genre_lower
    ]

@app.post('/bands')
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band