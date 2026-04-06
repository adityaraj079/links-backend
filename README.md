# LinkShoarder Backend

A Flask-based REST API for managing video links and profiles. Built with SQLite database and deployed on Vercel.

## 🚀 Features

- **Video Management**: Store and retrieve video links with titles, thumbnails, and tags
- **Profile Management**: Manage user profiles with names and pictures
- **Search Functionality**: Search videos by tags
- **CORS Enabled**: Supports cross-origin requests from frontend

## 🛠️ Tech Stack

- **Flask** - Web framework
- **SQLite** - Database
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library
- **OpenPyXL** - Excel file processing
- **BeautifulSoup4** - HTML parsing

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd links-backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   Create a `.env` file if you plan to use Google Images Search:
   ```
   API_KEY=your_google_api_key
   CSE_ID=your_custom_search_engine_id
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 🗄️ Database

The application uses SQLite with two main tables:

### Videos Table
```sql
CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    video_title TEXT,
    video_link TEXT,
    video_thumbnail TEXT,
    tags TEXT
);
```

### Profiles Table
```sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    name TEXT,
    picture TEXT
);
```

## 🌐 API Endpoints

### Videos
- `GET /get_links_with_titles` - Get all videos with metadata
- `POST /add_video` - Add a new video
  ```json
  {
    "title": "Video Title",
    "link": "https://example.com/video",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "tags": "tag1,tag2"
  }
  ```
- `GET /search_videos?tags=search_term` - Search videos by tags

### Profiles
- `GET /get_names` - Get all profiles
- `POST /add_profile` - Add a new profile
  ```json
  {
    "name": "Profile Name",
    "picture": "https://example.com/picture.jpg"
  }
  ```
- `GET /profile/<int:profile_id>` - Get specific profile

### Other
- `GET /get_video` - Get video content (deprecated)
- `GET /` - Welcome message

## 🚀 Deployment

### Vercel Deployment
1. **Connect GitHub repository** to Vercel
2. **Configure build settings**:
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`
3. **Environment Variables**: Set `API_KEY` and `CSE_ID` in Vercel dashboard (optional)
4. **Deploy**: Vercel will automatically detect the `vercel.json` configuration

**Note**: Database data is ephemeral in Vercel serverless functions. Added data will be lost between deployments. For persistent data, consider using a cloud database service.

### Local Development
```bash
python app.py
```
Server runs on `http://localhost:5000`

## 📊 Database Management

### Populate from Excel
```bash
python populate_db.py
```
This reads `links-new.xlsx` and populates the videos table.

### Manual Database Operations
The SQLite database `links.db` is created automatically on first run.

## 🔧 Configuration

### vercel.json
```json
{
    "version": 2,
    "builds": [
        {"src": "app.py", "use": "@vercel/python"}
    ],
    "routes": [
        {"src": "/(.*)", "dest": "app.py"}
    ]
}
```

### Environment Variables
- `API_KEY`: Google Custom Search API key
- `CSE_ID`: Google Custom Search Engine ID

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is private and proprietary.

## 📞 Support

For questions or issues, please create an issue in the repository.

