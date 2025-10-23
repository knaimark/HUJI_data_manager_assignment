# `models.py` is a Python script that creates a database named `era5` which can handle requests 
# similar to the one in `download_data.py`
# That is, downloading ERA5 Reanalysis hourly single-level data for: 
# - a certain date (that is, a one-day subset)
# - in a 1°×1° box around certain location
# - a specified list of variables
# The script implements `era5_ERD` with SQLAlchemy ORM

# Import SQLalchemy core objects (the needed classes from the core layer of SQLalchemy)
from sqlalchemy import (
    Integer, String, Float, Date, Text,
    Column, ForeignKey, UniqueConstraint, CheckConstraint, Index
)
# Import additional helpers from SQLalchemy.orm (Object Relational Mapper)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()



# Define the class `Variable` linked with the table `variable`
class Variable(Base):
    __tablename__ = "variable"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)      # optional text

    # Relationships: 
    # `Variable` to `Dataset`: many-to-many through the bridge table `dataset_variable`
    # `Variable` to `File`: one-to-many
    datasets = relationship("Dataset", secondary="dataset_variable", back_populates="variables")
    files = relationship("File", back_populates="variable")

    # Adjust the way the object is represented for more readability, 
    # as in <Variable(name=2m_temperature)>
    # Can be useful later for debugging
    def __repr__(self):         
        return f"<Variable(name={self.name})>"



# Define the class `Dataset` linked with the table `dataset`
class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    # Check constraints and create an index
    __table_args__ = (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="chk_latitude_range"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="chk_longitude_range"),
        Index("idx_dataset_location", "latitude", "longitude"),
    )

    # Relationships: 
    # `Dataset` to `Variable`: many-to-many through the bridge table `dataset_variable`
    # `Dataset` to `File`: one-to-many
    variables = relationship("Variable", secondary="dataset_variable", back_populates="datasets")
    files = relationship("File", back_populates="dataset")

    # Adjust the way the object is represented for more readability, 
    # as in <Dataset(lat=31.5, lon=35.0, date=2024-06-01)>
    # Can be useful later for debugging 
    def __repr__(self):       
        return f"<Dataset(lat={self.latitude}, lon={self.longitude}, date={self.date})>"



# Define the class `File` linked with the table `file`
class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    variable_id = Column(Integer, ForeignKey("variable.id"), nullable=False)
    path = Column(String, nullable=False)

    # Check constraints and create an index
    __table_args__ = (
        UniqueConstraint("dataset_id", "variable_id", name="uq_dataset_variable_file"),
        Index("idx_file_specs", "dataset_id", "variable_id"),
    )
    
    # Relationships: 
    # `File` to `Dataset`: many-to-one
    # `File` to `Variable`: many-to-one
    dataset = relationship("Dataset", back_populates="files")
    variable = relationship("Variable", back_populates="files")

    # Adjust the way the object is represented for more readability, 
    # as in <File(path=data/ERA5/2m_temperature_2024-06-01.nc)>
    # Can be useful later for debugging 
    def __repr__(self):         
        return f"<File(path={self.path})>"
    


# Define the class `DatasetVariable` linked with the bridge table `dataset_variable`
class DatasetVariable(Base):
    __tablename__ = "dataset_variable"

    # Both columns also act as FKs to `Dataset` and `Variable`
    # Composite PK = (dataset_id, variable_id) 
    # Notice that `File` has a UNIQUE constraint on the same pair
    dataset_id = Column(Integer, ForeignKey("dataset.id"), primary_key=True)
    variable_id = Column(Integer, ForeignKey("variable.id"), primary_key=True)



print("✅ Database created successfully.")        