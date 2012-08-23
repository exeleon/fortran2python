FFLAGS=  -O3 -r8 -w
EXENAME= crack
FC= ifort 

OBJS=\
modulo.o\
derivada.o\
memoria.o\
deriv_vel_tp.o\
jacob_malla.o\
tp_maker.o


$(EXENAME):  $(OBJS)
	$(FC)  $(OBJS) $(FFLAGS) -o $(EXENAME)
modulo.o: modulo.f90
	$(FC) $(FFLAGS) -c $*.f90
derivada.o: derivada.f90
	$(FC) $(FFLAGS) -c $*.f90
memoria.o: memoria.f90
	$(FC) $(FFLAGS) -c $*.f90
deriv_vel_tp.o: deriv_vel_tp.f90
	$(FC) $(FFLAGS) -c $*.f90
jacob_malla.o: jacob_malla.f90
	$(FC) $(FFLAGS) -c $*.f90
tp_maker.o: tp_maker.f90
	$(FC) $(FFLAGS) -c $*.f90
CLEAN :
	/bin/rm *.o
clean :
	/bin/rm *.o
