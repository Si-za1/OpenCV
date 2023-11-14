from datetime import date
from hbd.post_creation import PostCreation

data = [
    {"name": "John Timilsina", "image_path": "data/john.jpg"},
    {"name": "Alice Raj Prasad Acharya", "image_path": "data/alice.jpg"},
    {"name": "Harry Rai", "image_path": "data/harry.jpg"},
    {"name": "Pizza Poudel", "image_path": "data/pizza.jpeg"},
    {"name": "Apple Gurung", "image_path": "data/apple.jpeg"},
    {"name": "laptop Shrestha", "image_path": "data/laptop.jpeg"},
]

PostCreation().create_post(data)
