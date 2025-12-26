from app.models.users import User as UserModel
from app.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.db_depends import get_async_db
from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.schemas import Review as ReviewSchema

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/reviews", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return result.all()


@router.get("/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_reviews(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает все отзывы о товаре по его ID.
    """
    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    product = product_result.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return result.all()


@router.post("/reviews", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_reviews(data: ReviewSchema, db: AsyncSession = Depends(get_async_db),
                         current_user: UserModel = Depends(get_current_user)):
    """
    Создаёт новый отзыв (только для 'buyer').
    """
    if current_user.role != 'buyer':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only the buyer can create a review")

    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.id == data.product_id, ProductModel.is_active == True))
    if not product_result.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found or inactive")

    review = ReviewModel(
        user_id=current_user.id,
        product_id=data.product_id,
        comment=data.comment,
        grade=data.grade,
    )

    db.add(review)
    await db.commit()
    await update_product_rating(db, data.product_id)
    await db.refresh(review)
    return review


@router.delete("/reviews/{review_id}", response_model=ReviewSchema)
async def delete_review(
        review_id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: UserModel = Depends(get_current_user)
):
    """
    Выполняет мягкое удаление отзыва.
    """
    if current_user.id != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    result = await db.scalars(
        select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True)
    )
    review = result.first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive")

    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(review)
    return review


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()
