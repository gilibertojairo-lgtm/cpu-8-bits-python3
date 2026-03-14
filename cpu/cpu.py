import os

class CPU8Bit:
    def __init__(self, num_regs=4, mem_size=256):
        self.R = [0] * num_regs       # registros R0-R3
        self.memory = [0] * mem_size  # memoria de 256 bytes
        self.PC = 0                   # contador de programa
        self.running = False

    def load_program(self, filename):
        """
        Carga un archivo .bin en memoria.
        Cada línea debe ser un byte en binario de 8 bits.
        """
        if not filename.lower().endswith(".bin"):
            raise ValueError("Solo se permiten archivos .bin")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} no encontrado")

        with open(filename) as f:
            program = [int(line.strip(), 2) for line in f if line.strip()]

        # limpiar memoria y copiar programa al inicio
        self.memory = [0] * 256
        for i, b in enumerate(program):
            self.memory[i] = b

    def run(self):
        """Ejecuta el programa cargado en memoria"""
        self.PC = 0
        self.running = True

        while self.running:
            if self.PC >= len(self.memory):
                print("ERROR: PC fuera de memoria")
                break

            opcode = self.memory[self.PC]
            self.PC += 1

            # LOAD reg val
            if opcode == 1:
                reg = self.memory[self.PC]; self.PC += 1
                val = self.memory[self.PC]; self.PC += 1
                self.R[reg] = val

            # ADD regA regB
            elif opcode == 2:
                a = self.memory[self.PC]; self.PC += 1
                b = self.memory[self.PC]; self.PC += 1
                self.R[a] = (self.R[a] + self.R[b]) & 0xFF

            # SUB regA regB
            elif opcode == 3:
                a = self.memory[self.PC]; self.PC += 1
                b = self.memory[self.PC]; self.PC += 1
                self.R[a] = (self.R[a] - self.R[b]) & 0xFF

            # PRINT reg
            elif opcode == 4:
                reg = self.memory[self.PC]; self.PC += 1
                val = self.R[reg]
                if 32 <= val <= 126:
                    print(chr(val), end='')
                else:
                    print(val, end='')

            # PRINTSTR hasta 0
            elif opcode == 5:
                while True:
                    val = self.memory[self.PC]
                    self.PC += 1
                    if val == 0:
                        break
                    if 32 <= val <= 126:
                        print(chr(val), end='')
                    else:
                        print(val, end='')

            # STORE reg addr
            elif opcode == 6:
                reg = self.memory[self.PC]; self.PC += 1
                addr = self.memory[self.PC]; self.PC += 1
                self.memory[addr] = self.R[reg]

            # LOADM reg addr
            elif opcode == 7:
                reg = self.memory[self.PC]; self.PC += 1
                addr = self.memory[self.PC]; self.PC += 1
                self.R[reg] = self.memory[addr]

            # JMP addr
            elif opcode == 8:
                addr = self.memory[self.PC]
                self.PC = addr

            # JZ reg addr
            elif opcode == 9:
                reg = self.memory[self.PC]; self.PC += 1
                addr = self.memory[self.PC]; self.PC += 1
                if self.R[reg] == 0:
                    self.PC = addr

            # HALT
            elif opcode == 255:
                self.running = False

            else:
                print(f"ERROR: opcode {opcode}")
                self.running = False

        print()  # salto de línea final para separar del prompt
