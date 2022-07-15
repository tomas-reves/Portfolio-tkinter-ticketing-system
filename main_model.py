from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///tickets.db")
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "Tickets"

    id = Column(Integer, primary_key=True)
    rand_id = Column("No", String)
    title = Column("Title", String)
    date = Column("DateCreation", String)
    description = Column("Descr", String)
    status = Column("Status", String)
    status_date = Column("StatusDate", String)
    category = Column("Category", String)
    emp = Column("assignees", String)

    def __init__(self, rand_id, title, date, description, status, status_date, category, emp):
        self.rand_id = rand_id
        self.title = title
        self.date = date
        self.description = description
        self.status = status
        self.status_date = status_date
        self.category = category
        self.emp = emp

    def __str__(self):
        return f"{self.rand_id}, {self.title}, {self.date}, {self.description}, {self.status}, {self.status_date}, " \
               f"{self.category}, {self.emp}"


Base.metadata.create_all(engine)
