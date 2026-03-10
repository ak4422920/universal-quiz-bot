from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client.quizbot

users = db.users
chats = db.chats
questions = db.questions
books = db.books
sessions = db.sessions
tournaments = db.tournaments
challenges = db.challenges
badges = db.badges
logs = db.logs
