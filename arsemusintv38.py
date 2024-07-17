import sys

data = ""

if len(sys.argv) < 2:
	print("usage: arsemusint.py [infile]")
	exit()

with open(sys.argv[1], "r") as f:
	data = f.read()

lines = data.split("\n")
speed = 0
ins = []
patterns = []
data = []
index = 0
lastnote = 0
insno = 0
inc = True
insdefined = False
patternmode = False
channel = 0
atune = 438

data1 = []
data2 = []

def n2f(note):
	return (atune/32) * (2 ** ((note - 9) / 12))

def f2p(freq):
	return (int((32000/2) / freq)) & 0xFF

notes = (
	'c-', 'c#',
	'd-', 'd#',
	'e-',
	'f-', 'f#',
	'g-', 'g#',
	'a-', 'a#',
	'b-',
)

def parse(strn):
	note = strn[:2]
	octave = int(strn[-1])
	num = notes.index(note)
	num += 20
	num += (12 * (octave-1))
	num += 4
	return num

for i in lines:
	c = i.lower()
	if c.startswith("pattern"):
		patterns.append([])
		pno = int(c.split(" ")[1])
		patternmode = True
	elif c.startswith("pattend"): patternmode = False
	elif c.startswith("ch0"):
		for j in i.split(": ")[1].split(" "):
			data1.extend(patterns[int(j)])
	elif c.startswith("ch1"):
		for j in i.split(": ")[1].split(" "):
			hl = [h for h in patterns[int(j)] if h!=0]
			for p,q in zip(hl[::2], hl[1::2]):
				data2.extend([0,0] + [p,q])
		#z = 0
		#for j in i.split(": ")[1].split(" "):
			"""
			for a, b in enumerate(data):
				z += 1
				if b == 0:
					if z < len(patterns[int(j)]): data[a] = patterns[int(j)][z-3]
					else: z = 0
			"""
	if patternmode:
		if c[:2] in notes:
			print("note well found")
			index = 0
			insno = int(c.split(" ")[1])
			inc = True
			print(insno)
			for t in range(speed):
				lastnote = f2p(n2f(parse(c.split(" ")[0])))
				print(ins, insno, index)
				try: patterns[pno].extend([lastnote,ins[insno][index],0,0])
				except Exception:
					index = len(ins[insno]) - 1
					patterns[pno].extend([lastnote,ins[insno][index],0,0])
				index += 1
		elif c[:2] == '--':
			print("rest found")
			for t in range(speed):
				print(insno, index, t)
				if index > len(ins[insno]): inc = False
				try: patterns[pno].extend([lastnote,ins[insno][index],0,0])
				except Exception:
					index = len(ins[insno]) - 1
					patterns[pno].extend([lastnote,ins[insno][index],0,0])
				if inc:
					index += 1
	if c.startswith("tunebase"): atune = int(i.split(" ")[1])
	if c.startswith("speed"): speed = int(i.split(" ")[1])
	elif c.startswith("ins"):
		insdefined = True
		insnow = []
		for j in i.split(": ")[1].split(" "):
			insnow.append(int(j,base=16)+0x80)
		ins.append(insnow)
	elif c.startswith("#"): pass
	elif c.startswith("end"):
		data.extend([0xff] * 4)
		break
	if insdefined:
		if index > len(ins[insno]): index = 0

print(speed)
print(ins)
print(patterns)
print(data1)
print(data2)
data = [do or dt for do, dt in zip(data1,data2)]
with open("musix.arse","wb") as f:
	f.write(b"ARSE")
	f.write(bytearray(data))

