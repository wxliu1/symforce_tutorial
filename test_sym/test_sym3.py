
import symforce.symbolic as sf
from symforce.notebook_util import display

point = sf.V3.symbolic("p")
display(point)
display(point[:2])
string = "abcdefg"
display(string[:2])
display(string[3:])

