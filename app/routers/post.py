
from fastapi import FastAPI , Response,status, HTTPException, Depends,APIRouter
from .. import models, schemas , oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Path Operations
#Featching posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit:int =10,skip: int = 0 , search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts= cursor.fetchall()
    #print(limit)
    #posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return post


#creating an post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # to change the default status code 
def create_posts(post :schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #print(post.dict()) #convert pydantic model into dict
    #cursor.execute("""INSERT INTO posts ("Title","Content", "Published") VALUES (%s, %s, %s) RETURNING *  """,
    #                                (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

   
#featching only one perticular post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""Select * From posts where "ID"=%s""",(str(id)))
    #post = cursor.fetchone()
    #conn.commit()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post :
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {"error": f"post with {id} not found"}
        

#dellete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""Delete From posts where "ID"= %s returning *""",(str(id)))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not exist")

        #return {"message": "post is succesfully deleted"}
    if post.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action ")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    Response(status_code=status.HTTP_204_NO_CONTENT)
#to update the post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET "Title"= %s,"Content"= %s,"Published"= %s where "ID"=%s returning *""", (post.title, post.content, post.published,str(id)))
    
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)
    if post== None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not exist")
    
    if post.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action ")    

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()