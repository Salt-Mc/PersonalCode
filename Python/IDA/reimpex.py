
ea1 = SelStart()
ea2 = SelEnd()

ptrsz = 4

while ea1 < ea2:
	fncstrt = GetFunctionAttr(ea1, FUNCATTR_START)
	fncend = GetFunctionAttr(fncstrt, FUNCATTR_END)
	print(hex(fncstrt),hex(fncend))
	fncsz = fncend - fncstrt
	print(hex(fncsz))
	if fncsz == 0:
		break
	if fncsz == 0xa:
		op1 = GetMnem(fncstrt)
		op2 = GetMnem(fncstrt+5)
		if op1 == 'mov' and op2 == 'jmp':
			nameea = GetOperandValue(fncstrt,1)
			name = Name(nameea)
			if not MakeNameEx(fncstrt, name, SN_CHECK|SN_NOWARN):
				for  idx in range(99):
					if MakeNameEx(fncstrt, name + "_" + str(idx), SN_CHECK|SN_NOWARN):
						print("Made {} to {}".format(fncstrt, name))
						break;
			else:
				print("Made {} to {}".format(fncstrt, name))
		ea1 = fncend + 0x6
	else:
		break
