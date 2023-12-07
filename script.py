import sys, numpy as np

def parser(input_file = "scf.out",output_file = "POSCAR.vasp",type = "Cartesian"):    
    vectors = np.zeros((3,3),np.float64)
    at_spec = []
    at_numb=  []
    with open(input_file,"r") as f:
        while True:
            line = f.readline()
            if line.split() != []:
                if line.split()[0:2] == ["lattice","parameter"]:
                    alat = np.float64(line.split()[-2])*0.52917720859 
                    f.readline(); 
                    natoms = int(f.readline().split()[-1])
                    tatoms = int(f.readline().split()[-1])
                    at_pos = np.zeros((natoms,3),np.float64)
                elif line.split()[0] == "a(1)":
                    vectors[0,:] = alat * np.float64(line.split()[3:6])
                    vectors[1,:] = alat * np.float64(f.readline().split()[3:6])
                    vectors[2,:] = alat * np.float64(f.readline().split()[3:6])
                elif line.split()[0:2] == ["atomic","species"]:
                    for i in range(tatoms):
                        at_spec.append(f.readline().split()[0])
                elif line.split()[0:2] == ["Cartesian","axes"]:
                    if type == "Cartesian":
                        f.readline(); f.readline()
                        previous = at_spec[0]
                        for i in range(natoms):
                            l_ine = f.readline()
                            new = l_ine.split()[1]
                            
                            if new != previous:
                                at_numb.append(int(l_ine.split()[0])-1)

                            at_pos[i,:] = alat*np.float64(l_ine.split()[6:9])
                            previous = new
                        at_numb.append(int(l_ine.split()[0])-at_numb[-1])
                        break
                elif line.split()[0:2] == ["Crystallographic","axes"]:
                    if type != "Cartesian":
                        f.readline(); f.readline()
                        previous = at_spec[0]
                        for i in range(natoms):
                            l_ine = f.readline()
                            new = l_ine.split()[1]
                            
                            if new != previous:
                                at_numb.append(int(l_ine.split()[0])-1)

                            at_pos[i,:] = np.float64(l_ine.split()[6:9])
                            previous = new
                        at_numb.append(int(l_ine.split()[0])-at_numb[-1])
                        break   

    with open(output_file,"w") as f:

        f.write("Parsed from scf.out by Iriansr \n")
        f.write("1.0 \n")
        for i in range(3):
            f.write(str(vectors[i,:])[1:-1]+"\n")

        for ii,line in enumerate(at_spec):
            f.write(line+" ")
        f.write("\n")

        for ii,line in enumerate(at_numb):
            f.write(str(line)+" ")
        f.write("\n")

        if type == "Cartesian":
            f.write("Cartesian \n")
        else:
            f.write("Direct \n")
        for i in range(natoms):
            f.write(str(at_pos[i,:])[1:-1]+"\n")

