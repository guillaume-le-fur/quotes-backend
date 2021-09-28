from sqlalchemy import inspect
from db import db


# class BaseTable(db.Model):
#
#     def __init__(self, **kwargs):
#         # Setting the value of all the class attributes.
#         for key, val in kwargs.items():
#             setattr(self, key, val)
#
#     @classmethod
#     def row_exists(cls, **kwargs):
#         """
#         Check if at least one row exists for the given search parameters.
#
#         :param kwargs: The search arguments.
#         :return: True if at least one row is found, False otherwise.
#         """
#         return cls.query.filter_by(**kwargs).count() > 0
#
#     @classmethod
#     def get_attributes(cls, remove_id=True):
#         """
#         Returns the database column names.
#
#         :param remove_id: Should the column `id` be removed?
#         :return: The column names of the table.
#         """
#         lst = [elm.name for elm in inspect(cls).c]
#         if remove_id:
#             lst.remove('id')
#         return lst
#
#     @classmethod
#     def find_by_id(cls, _id: int) -> 'BaseTable':
#         return cls.find_by_attribute(id=_id)
#
#     @classmethod
#     def find_by_name(cls, name) -> 'BaseTable':
#         return cls.find_by_attribute(name=name)
#
#     @classmethod
#     def find_by_attribute(cls, **kwargs):
#         missing_attributes = []
#         attrs = cls.get_attributes()
#         for key in kwargs.keys():
#             if key not in attrs:
#                 missing_attributes.append(key)
#         if len(missing_attributes) > 0:
#             raise AttributeError(f'Missing the following attributes from table : {",".join(missing_attributes)}')
#         return cls.query.filter_by(**kwargs).first()
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
