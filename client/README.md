# React Native Client

## Setup

1. Start the backend API:
   ```bash
   cd ../backend
   uvicorn app.main:app --reload
   ```
   The API runs at `http://localhost:8000`.

2. Install dependencies for the client:
   ```bash
   cd ../client
   npm install
   ```

3. Run the app:
   ```bash
   npx react-native run-android
   ```

## Features

- **Login** – authenticate via `/users/login`.
- **Library** – lists books fetched from `/books`.
- **Reader** – select a book to fetch its markup and render it.

Use an account created via the backend to log in. After login, your stored books appear; tap one to view its markup.

