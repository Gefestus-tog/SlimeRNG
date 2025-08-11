# SlimeRNG

A fun slime collection game built with Django and vanilla JavaScript.

## Features

- **Slime Collection**: Spin the wheel to collect various types of slimes with different rarities
- **Crafting System**: Create powerful items using collected slimes
- **Collections**: Complete collections to earn rewards and bonuses
- **Leaderboards**: Compete with other players across multiple categories
- **Auto-save**: Your progress is automatically saved
- **Responsive Design**: Play on desktop or mobile devices

## Leaderboard Categories

The game features multiple leaderboard categories:

1. **Total Spins** 🎯 - Players with the most wheel spins
2. **Rare Slimes** ⭐ - Players who found the most rare slimes
3. **Total Slimes** 📦 - Players with the highest total slime count
4. **Completed Collections** 🏅 - Players who completed the most collections

## How to Play

1. Register or login to your account
2. Click the "SPIN!" button to collect slimes
3. Use collected slimes to craft items and complete collections
4. Check the leaderboards to see how you rank against other players
5. Click the "🏆 Таблица лидеров" button in the game to view leaderboards

## API Endpoints

- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login user
- `POST /api/logout/` - Logout user
- `POST /api/save/` - Save game progress
- `GET /api/load/` - Load game progress
- `GET /api/leaderboard/?type=<category>` - Get leaderboard data

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
5. Open `http://localhost:8000` in your browser

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (default)
- **Authentication**: Django Token Authentication
