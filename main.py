from fastapi import FastAPI, HTTPException
from schema import GenreURLChoices, Band

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
async def bands() -> list[Band]:
    return [
        Band(**b) for b in BANDS
    ]

@app.get('/bands/{band_id}')
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id), None)
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
async def bands_for_genre(genre: str) -> list[dict]:
    # Convert the input genre to lowercase
    genre_lower = genre.lower()
    
    # Validate if the lowercase genre is in the GenreURLChoices enum
    if genre_lower not in [g.value for g in GenreURLChoices]:
        raise HTTPException(status_code=400, detail=f"Invalid genre: {genre}. Valid genres are: {[g.value for g in GenreURLChoices]}")
    
    # Filter bands by the lowercase genre
    return [
        b for b in BANDS if b['genre'].lower() == genre_lower
    ]