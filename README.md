# FastAPI Experimentation

## Description
This project demonstrates the basics of FastAPI through a CRUD application that asynchronously stores data in a PostgreSQL database using SQLAlchemy and asyncio.

## Installation
1. Clone the repository.
2. Create a virtual environment and install dependencies from `requirements.txt`:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Install the latest version of PostgreSQL.
4. Create a database inside of PostgreSQL.
5. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql+asyncpg://user:pass@hostname/dbname
   USER_SECRET_KEY="some_random_key"
   ```

## Usage
6. Activate the virtual environment.
7. Run the application:
   ```
   python main.py
   ```
8. Access the interactive API documentation at `http://localhost:8000/docs`.
9. Register a user via the `/auth/register` endpoint under "auth".
10. Authorize using the button in the top-right corner.
11. Perform CRUD operations on Pokémon data via endpoints under the "pokemon" tag.

## References
This project is based on the Pokémon API repository: [farnswj1/PokemonAPI](https://github.com/farnswj1/PokemonAPI).