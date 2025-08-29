import machine, struct, time

cs = machine.Pin(17, machine.Pin.OUT)
sck = machine.Pin(18, machine.Pin.OUT)
mosi = machine.Pin(19, machine.Pin.OUT)
miso = machine.Pin(16, machine.Pin.IN)

useSoftSpi = False

if useSoftSpi:
    spi = machine.SoftSPI(
                  baudrate=10,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=sck,
                  mosi=mosi,
                  miso=miso)
else:
    spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=sck,
                  mosi=mosi,
                  miso=miso)

def write_reg(address, value):
    cs.value(0)
    spi.write(struct.pack('>B', 128 + address) + struct.pack('>B', value))
    cs.value(1)

def read_reg(address):
    cs.value(0)
    spi.write(struct.pack('>B', address))
    res, = struct.unpack('>B', spi.read(1))
    cs.value(1)
    return res


def test_video_mode(h_display, h_fporch, h_sync, h_bporch, v_display, v_fporch, v_sync, v_bporch):   
    write_reg(0, h_display // 256 + 64)  # visible
    write_reg(1, h_display % 256)
    write_reg(2, h_fporch // 256)
    write_reg(3, h_fporch % 256)
    write_reg(4, h_sync // 256 + 128)    # hsync high
    write_reg(5, h_sync % 256)
    write_reg(6, h_bporch // 256 + 32)   # next line
    write_reg(7, h_bporch % 256)
    write_reg(8, v_display // 256 + 64)  # visible
    write_reg(9, v_display % 256)
    write_reg(10, v_fporch // 256)
    write_reg(11, v_fporch % 256)
    write_reg(12, v_sync // 256 + 128)   # vsync high
    write_reg(13, v_sync % 256)
    write_reg(14, v_bporch // 256 + 32)  # next frame
    write_reg(15, v_bporch % 256)

def test_modeline(ml):
    acc = [int(i) for i in ml.split()[3:11]]

    test_video_mode(acc[0], acc[1]-acc[0], acc[2]-acc[1], acc[3]-acc[2],
                    acc[4], acc[5]-acc[4], acc[6]-acc[5], acc[7]-acc[6])


ml = 'Modeline "1024x768_69.81" 75.25 1024 1080 1184 1344 768 773 777 802 -HSync +VSync'

test_modeline(ml)
