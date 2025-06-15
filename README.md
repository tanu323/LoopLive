
# 📽️ Reels/Short Video Sharing App – FastAPI + React

A full-stack, real-time social video-sharing platform inspired by **Instagram Reels** and **Omegle**. Users can upload and share short videos, interact via likes and comments, and connect with strangers for live video calls.

---

## Features

## Authentication

- **Signup route**: `/auth/register`
- **Login route**: `/auth/login`
- Hash password using `passlib`
- Generate JWT token and return to frontend
- Auth middleware to protect routes (dependency that verifies JWT)

### 🎬 Short Video Creation
- Upload via **S3 Pre-signed URL**
- Draft editing (trim, filters, etc.)
- Finalize into published videos
- Control **privacy**, **tags**, and **featured** status

### 💬 Engagement & Discovery
- Like, comment, and view public videos
- Search videos by keyword or tag
- Featured and trending videos feed

### 📡 Live Video Matching (Omegle-style)
- WebRTC-based random video calls
- FastAPI WebSocket signaling for peer discovery
- Full signaling lifecycle (`offer`, `answer`, `ice`, etc.)

---

## 🧱 Architecture Overview

### 🖥️ Backend (FastAPI)
- **MongoDB** (via Motor)
- **JWT Auth** (with python-jose)
- **AWS S3** (boto3 for storage)
- **WebSockets** for real-time updates and calls
- Modular service-repository-router pattern

### 💻 Frontend (React)
- **React + Tailwind CSS**
- WebRTC integration
- JWT-based login flow
- Video feed with autoplay & infinite scroll

---

## 🗂️ Folder Structure

```bash
app/
├── api/
│   ├── video/                # Modular routers
│   └── deps.py               # Dependency injection
├── services/
│   └── video/                # create, manage, explore, interact
├── repositories/
│   └── video/                # Subrepositories + wrapper
├── models/                  # Pydantic models
├── schemas/                 # Request/response models
├── core/                    # Logging, enums, config
├── db/                      # MongoDB client
├── auth/                    # JWT utilities
└── main.py                  # App entrypoint
```

---

## 🔄 Modular API Routers

### `video_create_router.py`
- `POST /upload-url`
- `POST /drafts`
- `PATCH /drafts/{draft_id}`
- `POST /finalize`

### `video_manage_router.py`
- `DELETE /{video_id}`
- `PATCH /{video_id}/privacy`
- `PATCH /{video_id}/feature`
- `PATCH /{video_id}/details`

### `video_explore_router.py`
- `GET /{video_id}`
- `GET /user/{user_id}`
- `GET /stream/{video_id}`
- `GET /thumbnail/{video_id}`
- `GET /featured`
- `GET /search`
- `POST /{video_id}/views`

### `video_interact_router.py`
- `POST /{video_id}/like`
- `DELETE /{video_id}/unlike`
- `GET /{video_id}/likes`
- `POST /{video_id}/comment`
- `GET /{video_id}/comments`

---

## 🎥 Omegle-style Video Calling

### WebSocket Endpoint
`/ws/video-call`

### WebRTC Signaling Events
- `join_pool`, `match_found`
- `offer`, `answer`, `ice`
- `call_started`, `call_ended`, `disconnected`
- `Create `/ws` WebSocket endpoint`
- `Implement `ConnectionManager` for broadcasting real-time likes/comments`
- `Broadcast new comments/likes to relevant users`

---

### **Set Up AWS S3 for Video Upload**

- ` Use `boto3` to: `
   -`Upload videos`
   -`Generate signed URLs if needed`
   -` Store `s3_url` and optional `thumbnail_url` in MongoDB`

---

## 📜 OpenAPI Docs

All routes are documented via FastAPI's auto-generated OpenAPI spec:
```
http://localhost:8000/docs
```

Includes authentication, video endpoints, and WebSocket signaling examples.

---

## ✅ Milestone Checklist

| Feature                          | Status |
|----------------------------------|--------|
| JWT Auth                         | ✅     |
| User Profiles                    | ✅     |
| Upload via S3                    | ✅     |
| Video Drafting & Finalization    | ✅     |
| Likes & Comments                 | ✅     |
| Video Views & Search             | ✅     |
| Real-time WebSocket Signaling    | ✅     |
| Random WebRTC Calls              | ✅     |
| React Frontend                   | ⏳     |

---

## 📌 Next Steps

- [ ] Add moderation/reporting tools for video calls
- [ ] Group video chats
- [ ] Analytics dashboard for user engagement
- [ ] Dockerize for deployment with CI/CD

---

## 🧪 Testing & Deployment

- Test endpoints with `pytest` + `httpx`
- Add basic unit tests for key routes and logic
- Manual test with Postman
- Frontend integration with `axios` + WebRTC client

---


