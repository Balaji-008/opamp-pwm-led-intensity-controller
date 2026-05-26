import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='C:/Users/balaji/.gemini/antigravity/brain/73bf611f-a2b3-4671-8f13-c9be361abae5/circuit_diagram.png', show=False) as d:
    d.config(fontsize=11)
    
    # ---- STAGE 0: Virtual Ground Buffer ----
    d += elm.Line().length(1).label('12V', 'left')
    d += elm.Resistor().down().label('R3\n10kΩ')
    vg_node = d.here
    d += elm.Resistor().down().label('R4\n10kΩ')
    d += elm.Ground()
    
    d += elm.Line().right(1).at(vg_node)
    
    # op_buf: Buffer. in1=(-), in2=(+).
    # Input from divider goes to (+). So anchor to in2.
    op_buf = d.add(elm.Opamp(sign=True).fill('white').anchor('in2').label('LM324-D\n(Buffer)', 'center', ofst=[0, 0.5]))
    
    # Feedback from out to in1 (-)
    d += elm.Line().up(1.5).at(op_buf.out)
    d += elm.Line().left(2.5)
    d += elm.Line().down(1.5).to(op_buf.in1)
    
    # Output of buffer
    d += elm.Line().right(1.5).at(op_buf.out)
    d += elm.Dot()
    d.push()
    d += elm.Capacitor(polar=True).down().label('10µF')
    d += elm.Ground()
    d.pop()
    d += elm.Line().right(1)
    d += elm.Dot()
    d.push()
    d += elm.Capacitor().down().label('100nF')
    d += elm.Ground()
    d.pop()
    d += elm.Line().right(1.5).label('6V_BUF', 'right')


    # ---- STAGE 1: Schmitt Trigger ----
    d += elm.Line().right(2).at((op_buf.out.x + 8, op_buf.out.y + 4)).label('6V_BUF', 'left')
    d += elm.Resistor().right().label('R1\n10kΩ')
    d += elm.Dot()
    schmitt_in_ref = d.here
    
    # op_schmitt: positive feedback to (+). Reference input to (+).
    # Tri-wave input goes to (-).
    # Anchor `in2` to the reference.
    op_schmitt = d.add(elm.Opamp(sign=True).anchor('in2').fill('white').label('LM324-A\n(Schmitt)', 'center', ofst=[0, 0.5]))
    
    # Feedback R2 from OUT to in2 (+)
    d += elm.Line().up(1.5).at(schmitt_in_ref)
    d += elm.Resistor().right().label('R2\n20kΩ').tox(op_schmitt.out.x)
    d += elm.Line().down(1.5 + (op_schmitt.in1.y - op_schmitt.in2.y)).to(op_schmitt.out)
    d += elm.Dot()
    schmitt_out = d.here


    # ---- STAGE 2: Integrator ----
    d += elm.Line().right(1).at(schmitt_out).label('Square\nWave')
    d += elm.Resistor().right().label('R_in\n10kΩ')
    d += elm.Dot()
    int_in_minus = d.here
    
    # op_int: Integrator. Capacitor feedback to (-).
    # 6V_BUF goes to (+).
    # Anchor `in1` to the input resistor coming from schmitt out.
    op_int = d.add(elm.Opamp(sign=True).anchor('in1').fill('white').label('LM324-B\n(Integrator)', 'center', ofst=[0, -0.5]))
    
    # 6V_BUF to in2 (+)
    d += elm.Line().at(op_int.in2).left(1).label('6V_BUF', 'left')
    
    # Capacitor feedback for integrator (OUT to in1 [-])
    d += elm.Line().up(1.5).at(int_in_minus)
    d += elm.Capacitor().right().label('C_int\n100nF').tox(op_int.out.x)
    d += elm.Line().down(1.5).to(op_int.out)
    d += elm.Dot()
    int_out = d.here
    d += elm.Line().right(0.5).at(int_out).label('Triangle\nWave')
    
    # Connect Tri-wave back to Schmitt in1 (-)
    d += elm.Line().down(2).at(int_out)
    d += elm.Line().left().tox(op_schmitt.in1.x - 1)
    d += elm.Line().up().toy(op_schmitt.in1.y)
    d += elm.Line().right().to(op_schmitt.in1)


    # ---- STAGE 3: Comparator ----
    d += elm.Line().right(3).at(int_out)
    d += elm.Line().down(6)
    d += elm.Line().right(1).label('Triangle', 'left')
    triangle_node = d.here
    
    # op_comp: Comparator. Triangle goes to (-). V_sense goes to (+).
    # Anchor in1 (-) to the triangle input.
    op_comp = d.add(elm.Opamp(sign=True).anchor('in1').fill('white').label('LM324-C\n(Comp)', 'center', ofst=[0, 0.5]))
    d += elm.Line().left().at(op_comp.in1).to(triangle_node)
    
    # Sensor voltage divider for V_sense (+)
    d += elm.Line().down(3).at((op_comp.in2.x - 3, op_comp.in2.y))
    d += elm.Ground()
    d += elm.Photoresistor().up().label('LDR')
    d += elm.Dot()
    v_sense_node = d.here
    
    d += elm.Potentiometer().up().label('100kΩ Pot')
    d += elm.Line().up(0.5).label('12V', 'right')
    
    # Connect V_sense to in2 (+)
    d += elm.Line().right().at(v_sense_node).to(op_comp.in2).label('V_sense')
    

    # ---- STAGE 4: Power Driver ----
    d += elm.Line().right(1).at(op_comp.out).label('PWM')
    d += elm.Resistor().right().label('R_base\n4.7kΩ')
    
    q1 = d.add(elm.BjtNpn(circle=True).anchor('base').label('2N2222', 'right'))
    d += elm.Line().down(0.5).at(q1.emitter)
    d += elm.Ground()
    
    d += elm.Line().up(1).at(q1.collector)
    d += elm.LED().up().label('LED')
    d += elm.Resistor().up().label('R_led\n470Ω')
    d += elm.Line().up(0.5).label('12V', 'right')

