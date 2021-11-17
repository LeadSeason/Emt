import os
import sys
from dotenv import load_dotenv


load_dotenv()
print(os.environ.get("TOKEN"))
