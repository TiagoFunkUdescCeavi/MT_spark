from ArgumentReader import ArgumentReader
from App import App
import sys

app = App( ArgumentReader( sys.argv ) )
app.execute()
