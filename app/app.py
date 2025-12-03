from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="URL_HERE",
        file_type="photo",
        file_name="filename"
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    
    return {"posts": posts_data}

# text_posts = {
#     1: {"title": "Morning Routine", "content": "Wake up at 6 AM, exercise, have breakfast with coffee"},
#     2: {"title": "Shopping List", "content": "Milk, eggs, bread, vegetables, chicken"},
#     3: {"title": "Workout Plan", "content": "Run 5km, push-ups, squats, yoga session"},
#     4: {"title": "Book Recommendations", "content": "1984 by Orwell, To Kill a Mockingbird, Harry Potter series"},
#     5: {"title": "Travel Destinations", "content": "Paris, Tokyo, New York, Bali beaches"},
#     6: {"title": "Recipe Ideas", "content": "Pasta with tomato sauce, grilled cheese, salad with vinaigrette"},
#     7: {"title": "Goals for the Year", "content": "Learn a new language, read 20 books, save money for trip"},
#     8: {"title": "Movie Watchlist", "content": "Inception, The Matrix, Shawshank Redemption"},
#     9: {"title": "Garden Tips", "content": "Water plants daily, use fertilizer, prune regularly"},
#     10: {"title": "Pet Care", "content": "Feed twice a day, walk the dog, vet checkup monthly"},
#     11: {"title": "Study Schedule", "content": "Math from 9-11, break, Science from 12-2"},
#     12: {"title": "Party Planning", "content": "Invite friends, buy decorations, prepare snacks"},
#     13: {"title": "Budget Tracker", "content": "Rent $1000, groceries $300, entertainment $150"},
#     14: {"title": "Fitness Goals", "content": "Lose 10 pounds, build muscle, improve flexibility"},
#     15: {"title": "DIY Projects", "content": "Build a shelf, paint the room, fix the leaky faucet"},
#     16: {"title": "Music Playlist", "content": "Rock classics, pop hits, jazz for relaxation"},
#     17: {"title": "Health Tips", "content": "Drink water, eat fruits, sleep 8 hours"},
#     18: {"title": "Vacation Ideas", "content": "Beach resort, mountain hiking, city exploration"},
#     19: {"title": "Journal Entry", "content": "Reflected on the day, grateful for family and friends"},
#     20: {"title": "Tech Gadgets", "content": "New smartphone, wireless earbuds, smartwatch"}
# }

# @app.get("/posts")
# def get_all_posts(limit: int = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts

# @app.get("/posts/{id}")
# def get_post(id: int) -> PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found.")

#     return text_posts.get(id)

# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post



# @app.get("/hello-world")
# def hello_world():
#     return {"messsage": "Hello, World! My name is Ryan!"}

