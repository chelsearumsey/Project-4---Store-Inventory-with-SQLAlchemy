
from models import (Base, session,
                    Inventory, engine)
import csv
import datetime
import time


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
