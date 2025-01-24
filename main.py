from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import GenreURLChoices, BandBase, BandCreate, Band, Album
from typing import Annotated
from sqlmodel import Session, select
from db import init_db, get_session

app = FastAPI()

@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    band_list = session.exec(select(Band)).all()

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
async def band(
    band_id: Annotated[int, Path(title='Band ID')],
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        #status code 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band

# @app.get('/bands/all/{genre}')
# async def bands_genre_available(genre: GenreURLChoices) -> dict:
#     matching_bands = [b['name'] for b in BANDS if b['genre'].lower() == genre.value]

#     if not matching_bands:
#         #status code 404
#         raise HTTPException(status_code=404, detail=f"No bands found for {genre}")
#     numbered_bands = [f"{i+1}. {name}" for i, name in enumerate(matching_bands)]
#     return {"bands": numbered_bands}

# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
#     # Convert the input genre to lowercase
#     genre_lower = genre.lower()
    
#     # Validate if the lowercase genre is in the GenreURLChoices enum
#     if genre_lower not in [g.value for g in GenreURLChoices]:
#         raise HTTPException(status_code=400, detail=f"Invalid genre: {genre}. Valid genres are: {[g.value for g in GenreURLChoices]}")
    
#     # Filter bands by the lowercase genre
#     return [
#         b for b in BANDS if b['genre'].lower() == genre_lower
#     ]

@app.post('/bands')
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title= album.title, release_date=album.release_date, band=band
            )
            session.add(album_obj)
    
    session.commit()
    session.refresh(band)
    return band