# ImagiMatrix
This is a repository to consolidate all the ML utilities in one place.

💫 **Version 0.0.1**


## Installation

Install the repository via python to your python environment

```bash
pip install imagi-matrix
```

## Included in this repository

<ul>
<li>[x] Birthday Post Creator </li>
</ul>


## Birthday Post Creator

```python
from datetime import date
from hbd.post_creation import PostCreation

data = [
    {"name": "John Timilsina", "DOB": date(1990, 11, 13), "image_path": "data/john.jpg"},
    {"name": "Alice Raj Prasad Acharya", "DOB": date(1985, 11, 13), "image_path": "data/alice.jpg"},
    {"name": "Harry Rai", "DOB": date(1955, 11, 13), "image_path": "data/harry.jpg"},
    {"name": "Pizza Poudel", "DOB": date(1990, 11, 13), "image_path": "data/pizza.jpeg"},
    {"name": "Apple Gurung", "DOB": date(1985, 11, 13), "image_path": "data/apple.jpeg"},
    {"name": "laptop Shrestha", "DOB": date(1955, 11, 13), "image_path": "data/laptop.jpeg"},
]

PostCreation().create_post(data)
```