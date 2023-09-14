from datetime import datetime

from flask_jwt_extended import current_user
from sqlalchemy import desc

from src import db
from src.common.handle_exception import NotFoundException, BadRequestException
from src.common.validate import ValidateObjectExistByID
from src.models import Book, User


class BookService:
    @staticmethod
    def get_list_book_by_search_params(params):  # noqa C901
        search = (
            "%{}%".format(params.get("search").strip())
            if params.get("search")
            else None
        )
        page = params.get("page") or 1
        size = params.get("size") or 20

        query = (
            Book.query.join(User, Book.author_id == User.id)
            .distinct()
            .filter(Book.deleted_date.is_(None))
        )
        last_update = (
            Book.query.filter(Book.updated_date.isnot(None))
            .order_by(Book.updated_date.desc())
            .first()
        )

        if search:
            query = query.filter(Book.title.ilike(search) | User.username.ilike(search))

        total = query.count()
        books = (
            query.order_by(desc(Book.updated_date))
            .paginate(page=int(page), per_page=int(size), error_out=False)
            .items
        )

        response_data = []
        for book in books:
            book_dict = {
                "id": book.id,
                "title": book.title,
                "author_name": book.author.username,
                "pages_num": book.pages_num,
                "review": book.review,
                "rate": book.rate,
                "title_author": book.title_author,
            }
            response_data.append(book_dict)

        return {
            "items": response_data,
            "page_size": int(size),
            "page": int(page),
            "total": total,
            "last_update": last_update.updated_date if last_update else None,
        }

    @staticmethod
    def create_book(data):
        # check if given name is already exists in db, if they do, throw error
        book_check_duplicate_name = Book.query.filter(
            Book.title == data.get("title")
        ).first()
        if book_check_duplicate_name is not None:
            raise BadRequestException(
                message=f"Book with name '{data.get('title')}' already exists"
            )

        # check if author id exists in table user, if not, throw error
        validator = ValidateObjectExistByID()
        validator(User, id=data.get("author_id"), name="author_id")

        book = Book(
            title=data.get("title"),
            author_id=data.get("author_id"),
            pages_num=data.get("pages_num"),
            review=data.get("review"),
            rate=data.get("rate"),
            created_date=datetime.utcnow(),
            created_by=current_user.id,
            updated_date=datetime.utcnow(),
            updated_by=current_user.id,
        )
        db.session.add(book)
        db.session.commit()

        response_data = {
            "id": book.id,
            "title": book.title,
            "author_id": book.author_id,
            "pages_num": book.pages_num,
            "review": book.review,
            "rate": book.rate,
        }

        return response_data

    @staticmethod
    def get_book_by_id(id: int):
        book: Book = db.session.query(Book).filter(Book.id == id).first()
        if book is None:
            raise NotFoundException(message=f"Book with id: {id} not found")

        return {
            "id": book.id,
            "title": book.title,
            "author_name": book.author.username,
            "pages_num": book.pages_num,
            "review": book.review,
            "rate": book.rate,
        }

    @staticmethod
    def update_book(data, id: int):  # noqa: C901
        # check if book with given id exists in table book, if not, throw error
        book = Book.query.get(id)
        if book is None:
            raise NotFoundException(message=f"Book with id {id} not found")

        # check if author id exists in table user, if not, throw error
        validator = ValidateObjectExistByID()
        validator(User, id=data.get("author_id"), name="author_id")

        # check if given name is already exists in db, if they do, throw error
        # we only check for other records, not the record with given id
        # that why we have additional filter Book.id != id
        book_check_duplicate_name = Book.query.filter(
            Book.title == data.get("title"), Book.id != id
        ).first()
        if book_check_duplicate_name is not None:
            raise BadRequestException(
                message=f"Book with name '{data.get('title')}' already exists"
            )

        book.title = data.get("title")
        book.author_id = data.get("author_id")
        book.pages_num = data.get("pages_num")
        book.review = data.get("review")
        book.rate = data.get("rate")
        book.updated_date = datetime.utcnow()
        book.updated_by = current_user.id

        db.session.commit()

        return {
            "id": book.id,
            "title": book.title,
            "author_name": book.author.username,
            "pages_num": book.pages_num,
            "review": book.review,
            "rate": book.rate,
        }

    @staticmethod
    def delete_book(id: int):
        if id:
            book = Book.query.filter(
                Book.id == id,
                Book.deleted_date.is_(None),
                Book.deleted_by.is_(None),
            ).first()

            if book is None:
                raise NotFoundException(message=f"Book with id {id} not found")

            book.deleted_date = datetime.utcnow()
            book.deleted_by = current_user.id
            db.session.add(book)
            db.session.commit()
