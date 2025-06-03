from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    following: Mapped[List["Follower"]] = relationship("Follower",
        foreign_keys="Follower.user_from_id",
        back_populates="user_from")
    followers: Mapped[List["Follower"]] = relationship("Follower",
        foreign_keys="Follower.user_to_id",
        back_populates="user.to")
  
class Follower(db.Model):
    __tablename__='follower' 
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)
    user_from: Mapped["User"] = relationship("User",
        foreign_keys=[user_from_id],
        back_populates="following")
    user_to: Mapped["User"] = relationship("User",
        foreign_keys=[user_to_id],
        back_populates="followers")

class Post(db.Model):
    __tablename__='post' 
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")

class Comment(db.Model):    
    __tablename__='comment'  
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["User"] = relationship("User")

class Media(db.Model):
    __tablename__='media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped["Post"] = relationship("Post", back_populates="media")








    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
