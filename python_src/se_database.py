import random

def generate_slug(word_list, num_words=3):
    return "-".join(random.sample(word_list, num_words))

# Example usage
words = [
    "luxury", "escape", "retreat", "paradise", "hideaway",
    "exclusive", "resort", "getaway", "haven", "sanctuary",
    "bliss", "oasis", "adventure", "journey", "holiday",
    "voyage", "tranquil", "seaside", "island", "hideout"
]

# In-memory database
class InMemoryDatabase:
    def __init__(self):
        self.records = []

    def add_record(self, record_id, url_slug):
        self.records.append({"id": record_id, "url_slug": url_slug})

    def get_record_by_id(self, record_id):
        for record in self.records:
            if record["id"] == record_id:
                return record
        return None

# Initialize database and add records
db = InMemoryDatabase()
for i in range(1, 6):
    slug = generate_slug(words)
    db.add_record(i, slug)
