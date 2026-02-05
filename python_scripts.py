from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins, including local files
    allow_methods=["*"],
    allow_headers=["*"],
)