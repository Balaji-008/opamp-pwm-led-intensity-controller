import schemdraw
import schemdraw.elements as elm
with schemdraw.Drawing(file='C:/Users/balaji/Downloads/EC2lab/test_opamp.png', show=False) as d:
    op = d.add(elm.Opamp())
